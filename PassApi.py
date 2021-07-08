import requests
import hashlib
import sys

def requestApi(data):
        
    url = 'https://api.pwnedpasswords.com/range/' + data
    res = requests.get(url)

    if res.status_code !=200:
        raise RuntimeError(f'Error fetching {res.status_code},Check api')
    
    return res

def getPassLeakCount(hashes,hash_to_check):

    hashes = (line.split(':') for line in hashes.text.splitlines() )

    for hash,count in hashes:
        
        if(hash==hash_to_check):
            return count

    return 0

def checkPass(password):

    # print(hashlib.sha1(password.encode('utf-8')))
    # print(hashlib.sha1(password.encode('utf-8')).hexdigest() )
    # print(hashlib.sha1(password.encode('utf-8')).hexdigest().upper() )

    sha1pass=hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail=sha1pass[:5],sha1pass[5:]

    response = requestApi(first5_char)

    return getPassLeakCount(response,tail)
    
def main(args):

    for password in args:
        count = checkPass(password)

        if(count):
            print(f'{password} was found {count} times. We recommends you to change your password')
        else:
            print(f'{password} wasen\'t found. Carry on......  ')

    return 'done'

main(sys.argv[1:])

'''
We need to give input from file contaning passwords.
To make it more secure
'''
