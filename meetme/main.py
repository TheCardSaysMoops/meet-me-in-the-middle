import requests
from pandas import DataFrame

# documentation: "https://developers.amadeus.com/self-service/category/air/api-doc/flight-inspiration-search/api-reference" 

class FlightFrame:
    def __init__(self, api_key, api_secret):
        # initialize the class by getting a token from Amadeus
        # you'll need to pass in your API key & API secret supplied by Amadeus
        self.endpoint = "https://api.amadeus.com/v1/security/oauth2/token"
        self.token_data = {
            'grant_type': 'client_credentials',
            'client_id': api_key,
            'client_secret': api_secret
            }
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        # get token and apply to class
        self._get_token()
    
    def _get_token(self):
        token_object = requests.post(url=self.endpoint, data=self.token_data, headers=self.headers)
        # check if valid token
        if token_object.status_code == 200:
            self.token = token_object.json().get("access_token")
        else:
            raise ValueError(token_object.json())
    
    def _get_response(self, origin, departureDate, duration, nonStop, oneWay):
        # set data to be used in API get call
        url = r'https://api.amadeus.com/v1/shopping/flight-destinations'
        params = {
            'origin': origin,
            'departureDate': departureDate,
            'duration': duration,
            'nonStop': nonStop,
            'oneWay': oneWay
            }
        headers={'Authorization': f'Bearer {self.token}'}

        # return a requests object given the supplied parameters
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 401:
            self._get_token()
            response = requests.get(url, params=params, headers=headers)
        else:
            raise ValueError(response.json())

    def _get_flight_attribute(self, response, attribute):
        # create list for the given data point, e.g. flight prices
        attribute_list = [data.get(attribute) for data in response.json().get('data')]
        return attribute_list   


    def _get_destination_details(self, origin, departureDate, duration, nonStop, oneWay):
        # get response object for the desired origin
        response = self._get_response(origin, departureDate, duration, nonStop, oneWay)
        
        # get information on the flights from the desired origin
        origins = self._get_flight_attribute(response, 'origin')
        destinations = self._get_flight_attribute(response, 'destination')
        departure_dates = self._get_flight_attribute(response, 'departureDate')
        return_dates = self._get_flight_attribute(response, 'returnDate')
        prices = [price['total'] for price in self._get_flight_attribute(response, 'price')]

        # create a dictionary with the flight information to be stored in a Pandas DataFrame
        flight_dict = {
                'origin': origins,
                'destination': destinations,
                'departure_date': departure_dates,
                'return_date': return_dates,
                'price': prices
                }
        
        flight_types = {
                'origin': str,
                'destination': str,
                'departure_date': str,
                'return_date': str,
                'price': float
                }

        # create Pandas DataFrame from the flight information dictionary
        flight_df = DataFrame(flight_dict)
        flight_df = flight_df.astype(flight_types)
        
        return flight_df

    def lets_meet(self, origin1, origin2, departureDate=None, duration=None, nonStop='false', oneWay='false'):
        """
        Create a table of lowest price destinations
        given 2 origin cities

        Parameters
        ----------
        origin1 : [str]
            airport IATA code of first origin city
        origin2 : [str]
            airport IATA code of second origin city
        departureDate : [str]
            date of departure in 'YYYY-MM-DD' format
            e.g. '2020-01-01'
        duration : [int]
            number of days of trip
        nonStop : [boolean]
            'true' for non-stop trips only
            'false' flights with layovers allowed
        oneWay : [boolean]
            'true' for one way trips
            'false' for round trip
        
        Returns
        -------
        Pandas dataframe with flight prices from both origin
        cities sorted by lowest combined flight price
        """
        
        
        # get Pandas DataFrames for the two origins
        self.flight_df1 = self._get_destination_details(origin1, departureDate, duration, nonStop, oneWay)
        self.flight_df2 = self._get_destination_details(origin2, departureDate, duration, nonStop, oneWay)

        # join the two DataFrames together
        self.combined_flights = self.flight_df1.merge(self.flight_df2, on = "destination", suffixes = (f'_{origin1}', f'_{origin2}'))

        # add the two fares together to get a combined fare
        self.combined_flights["combined_price"] = self.combined_flights[f'price_{origin1}'] + self.combined_flights[f'price_{origin2}']

        # sort on combined price
        self.combined_flights.sort_values("combined_price")
        
        return(self.combined_flights)