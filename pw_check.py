import requests
import hashlib
from sys import argv



def hashing(pw):
    hash_pw = hashlib.sha1(pw.encode('utf-8')).hexdigest().upper()
    return hash_pw

def request_api_data(hashed_pw):
    url = 'https://api.pwnedpasswords.com/range/' + hashed_pw[:5]
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res

def unpack_api_data(data, hashed_pw):
    data_tuple = (x.split(':') for x in data.text.splitlines())
    return data_tuple

def check_hash_matches(hashed_pw, unpacked_data, password):
    for hash, count in unpacked_data:
        if hashed_pw[5:] == hash:
            return (f'Your password ({password}) has been leaked {count} times!You should change your password!')

    return (f'Your password ({password}) has not been leaked!You are good!')

if __name__=='__main__':
    for x in argv[1:]:
        hash = hashing(x)
        data = request_api_data(hash)
        unpacked_data = unpack_api_data(data, hash)
        resolve = check_hash_matches(hash, unpacked_data, x)
        print(resolve)