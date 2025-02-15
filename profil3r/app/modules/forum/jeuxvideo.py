from profil3r.app.search import search_get
from bs4 import BeautifulSoup
import time

class Jeuxvideo:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['jeuxvideo']['rate_limit'] / 1000
        # https://www.jeuxvideo.com/profil/{}?mode=infos
        self.format = config['plateform']['jeuxvideo']['format']
        # Jeuxvideo.com usernames are not case sensitive
        self.permutations_list = [perm.lower() for perm in permutations_list]
        # Forum
        self.type = config['plateform']['jeuxvideo']['type']

    # Generate all potential jeuxvideo.com usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        jeuxvideo_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            r = search_get(username)
            if not r:
                continue
            
            # If the account exists
            if r.status_code == 200:
                # Account object
                account = {}

                # Get the username
                account["value"] = username
                
                # Parse HTML response content with beautiful soup 
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Scrape the user description
                try:
                    user_description = str(soup.find_all(class_='bloc-description-desc')[0].get_text()) if soup.find_all(class_='bloc-description-desc') else None
                    account["description"] = {"name": "Description", "value": user_description}
                except:
                    pass
                
                # Scrape the user signature
                try:
                    user_signature = str(soup.find_all(class_='bloc-signature-desc')[0].find_all("p")[1].get_text()) if soup.find_all(class_='bloc-signature-desc') else None
                    account["signature"] = {"name": "Signature", "value": user_signature}
                except:
                    pass

                # Scrape the user informations
                try:
                    informations_correspondances = {
                        "Age": "age",
                        "Pays": "country",
                        "Pays / Ville": "country_city",
                        "Genre": "gender",
                        "Membre depuis": "inscription",
                        "Messages Forums": "messages_count",
                        "Commentaires": "comments",
                        "Dernier passage": "last_connection"

                    }

                    user_informations = soup.find_all(class_='bloc-default-profil')[0].find_all("li")
                    for information in user_informations:
                        information = [str(' '.join(info.strip().split())) for info in information.get_text().split(":")]
                        account[informations_correspondances[information[0]]] = {"name": information[0], "value": information[1]}

                except:
                    pass
                
                # Append the account to the accounts table
                jeuxvideo_usernames["accounts"].append(account)

            time.sleep(self.delay)
        
        return jeuxvideo_usernames