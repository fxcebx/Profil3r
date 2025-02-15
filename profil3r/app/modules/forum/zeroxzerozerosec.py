from profil3r.app.search import search_get
import time

class Zeroxzerozerosec:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['zeroxzerozerosec']['rate_limit'] / 1000
        # https://0x00sec.org/u/{username}
        self.format = config['plateform']['zeroxzerozerosec']['format']
        # 0x00sec.org usernames are not case sensitive
        self.permutations_list = [perm.lower() for perm in permutations_list]
        # Forum
        self.type = config['plateform']['zeroxzerozerosec']['type']

    # Generate all potential 0x00sec usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        zeroxzerozerosec_usernames = {
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
                zeroxzerozerosec_usernames["accounts"].append({"value": username})
            time.sleep(self.delay)
        
        return zeroxzerozerosec_usernames