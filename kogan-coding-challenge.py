"""Solution to Kogan Coding Challenge[https://kogan-recruitment.herokuapp.com/challenge/6b463a3d03043748ff92a8caf59393d4/]
   Position: Full Stack Developer

   @author: Akshay Salunke
"""

import requests
import json

class KoganChallenge:
    """Solution for Kogan Coding Challenge - FSDEV2020

    Raises:
        KeyError: If 'objects' not found in response.
    """
    BASE_URL = 'http://wp8m3he1wt.s3-website-ap-southeast-2.amazonaws.com'
    ENDPOINT = '/api/products/1'
    INDUSTRY_CUBIC = 250
    total_acs = 0
    total_cubic_weight = 0

    def start(self):
        self.fetch_data()
        self.print_results()

    def fetch_data(self):
        """Fetch data from URL

        Raises:
            RequestException: If there is an problem sending http request.
            JSONDecodeError: If API returns malformed json.
        """
        url = self.BASE_URL + self.ENDPOINT
        while(url is not None):
            try:
                response = requests.get(url)
                response.raise_for_status()
                response_data = json.loads(response.text)
            except requests.exceptions.RequestException as e:
                print("An error occured while fetching data from api.", e)
                raise
            except json.JSONDecodeError as e:
                print("Error parsing json response.", e)
                raise
            
            self.process_data(response_data)

            next_url = response_data['next']
            if next_url:
                url = self.BASE_URL + next_url
            else:
                url = None

    def process_data(self, response):
        """Process the http response to calculate 'Average Cubic Weight' of all 'Air Conditioners'

        Args:
            response (json): API response to parse

        Raises:
            KeyError: If 'objects' key is not in response
        """
        if 'objects' not in response:
            raise KeyError("'objects' key not found in response")
        for item in response['objects']:
            if 'air conditioners' in item['category'].lower():
                self.total_acs += 1
                size = item['size']  # in cm
                item_volume = (size['length'] * size['width'] * size['height']) / (100 * 100 * 100) # Convert cm^3 to m^3
                # Multiply by 250 kg/m^3 (Industry Standard)
                self.total_cubic_weight += (item_volume * self.INDUSTRY_CUBIC)

    def print_results(self):
        """Print final results
        """
        print('Average Cubic Weight of {a} ACs: '.format(a=self.total_acs), round(self.total_cubic_weight/self.total_acs, 3), 'kg')


if __name__ == "__main__":
    kg = KoganChallenge()
    kg.start()
