import time
import os.path
from os import path

import requests



class HabiticaAccess:
    def __init__(self):
        self.TOKEN_PATH = "secrets/habitica_apiToken.txt"

    def get_token(self):
        if path.exists(self.TOKEN_PATH): # if previous token been made
            print(str(time.time()) + ": found an old token")
            with open(self.TOKEN_PATH, "r") as f:
                old_token = [i for i in f]
                print("This is old token", old_token)
            if float(old_token[0]) < time.time(): # If old token is expired make new one
                print(str(time.time()) + ": found an old token expired token")
                new_token = str(time.time() + 3600) + "\n"
                new_token += self.get_new_api_token()
                with open(self.TOKEN_PATH, "w+") as f:
                    f.write(new_token)
                return new_token
            else: # Old token is still good
                print(str(time.time()) + ": found an old token that still works")
                return old_token[1] 

        else:
            print(str(time.time()) + ": found no old token")
            with open(self.TOKEN_PATH, "w+") as f:
                new_token = str(time.time() + 3600) + "\n" + self.get_new_api_token()
                f.write(new_token)
                print("Writing to new token")
            return new_token

    
    def get_new_api_token(self):
        """
        DO NOT CALL THIS FUNCTION DIRECTLY
        IT SHOULD BE CALLED ONLY FROM get_token()

        Logs the Habtica user and stores an api token on file
        """
        with open("secrets/habitica_username.txt") as f:
            HABITICA_USERNAME = f.read().strip()
        with open("secrets/habitica_password.txt") as f:
            HABITCA_PASSWORD = f.read().strip()

        if not HABITICA_USERNAME or not HABITCA_PASSWORD:
            print("Make sure that you make files, secrets/habitica_password.txt, secrets/habitica_username.txt")
            raise FileNotFoundError()

        print(HABITICA_USERNAME, HABITCA_PASSWORD)

        # client_auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_SECRET)
        post_data = {'username':HABITICA_USERNAME, 'password':HABITCA_PASSWORD}
        headers = {"User-Agent": "Habitica Leetcode Handler by afloresescarcega"}
        # response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
        # response = requests.post("https://ssl.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
        response = requests.post('https://habitica.com/api/v3/user/auth/local/login', data=post_data, headers=headers)

        print()
        print(response.json())
        print()
        habitica_token = response.json()['data']['apiToken']
        print("This is habitica token: ", habitica_token)
        with open("secrets/habitica_apiToken.txt", "w") as f:
            f.write(habitica_token)
        return habitica_token


r = requests.post('https://habitica.com/api/v3/user/auth/local/login', data = {'key':'value'})

if __name__ == '__main__':
    token_handler = HabiticaAccess()
    token_handler.get_token();