"""
Functions to implement:
    Add/delete/update/view passwords
    strength checker
    password generator


Database:
Tables:
    master  (id, pass, verKey(KDF))
    data    (username/email,  encPass(AES 256),  website,  website login page URL)
    log     (action, uID)

    

Libraries:
    generator:          secret, random
    strength:           zxcvbn    
    cryptography:       encryption/decryption.
    pyotp (Optional):   MFA.
"""

import sqlite3
import secrets
import random
# import zxcvbn
import cryptography
import pyotp


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



db_connection = sqlite3.connect("passwords_DB.db")

def database_and_tables():
    print("Alhamdulillah! db created")

    db_connection.execute("""CREATE TABLE IF NOT EXISTS master(     
                 username VARCHAR(30) PRIMARY KEY,
                 verification_key TEXT
    );
    """)

    db_connection.execute("""CREATE TABLE IF NOT EXISTS credentials(
                 username_or_email VARCHAR(30) NOT NULL,  
                 encrypted_pass TEXT,  
                 website TEXT,  
                 website_URL TEXT,
                 CONSTRAINT pk_constraint PRIMARY KEY (username_or_email, website)         
    );
    """)
    db_connection.close()



def add_password():
    print("add password")


def delete_password():
    print("delete password")


def update_password():
    print("update password")


def view_password():
    print("view password")


def kdf(master_password, salt_type):
    # salt_string = "unpredictable"
    salt_bytes = salt_type.encode() 

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  
        salt= salt_bytes,
        iterations=390000, 
    )

    key = kdf.derive(master_password.encode()) 
    return key


def insert_into_master(username, verification_key):
    query = "INSERT INTO master (username, verification_key) VALUES(?,?)"
    db_connection.execute(query, (username, verification_key))
    db_connection.commit()


def verification(username, verification_key):
    query = "SELECT verification_key FROM master WHERE username = ?"
    cursor = db_connection.cursor()

    try:
        cursor.execute(query, (username,))
        record = cursor.fetchone()
        print(record[0])
        if verification_key == record[0]:
            print("vrerified")
        else:
            print("Unauthorized")
        return record
    except sqlite3.Error as error:
        print("Error while verification : ", error)
        return None
    finally:
        cursor.close()



def sign_up():
    username = input("Enter a username (MUST BE UNIQUE) : ")
    #check if alr exist (DB)

    master_password = input("Enter a strong master password (specify characteristics): ")
    #strength condition verify 

    verification_salt = "salt_4_ver"
    verification_key = kdf(master_password, verification_salt)
    # print(verification_key)
    insert_into_master(username, verification_key)
    # verification(username, verification_key)

    encryption_salt = "salt_4_enc"
    encryption_key = kdf(master_password, encryption_salt)
    # print(encryption_key)


def sign_in():
    username = input("Enter your username : ")
    #check if alr exist (DB)

    master_password = input("Enter your master password (acc to the specified characteristics): ")
    #strength condition verify 

    verification_salt = "salt_4_ver"
    verification_key = kdf(master_password, verification_salt)
    print(verification_key)
    # insert_into_master(username, verification_key)
    verification(username, verification_key)

    encryption_salt = "salt_4_enc"
    encryption_key = kdf(master_password, encryption_salt)
    # print(encryption_key)



def main():
    print("main")
    # database_and_tables()
    sign_up()
    # sign_in()


    # LASTTTTTTTTTTTTTTT
    db_connection.close()



if __name__ == "__main__":
    main()





"""

Master Password:
    - Don't store the master password itself in the database.
    - Consider using a technique like key derivation function (KDF) to generate a key from the master password that's used for encryption/decryption.


MFA (Optional):
    - Explore libraries like pyotp to integrate Multi-Factor Authentication using one-time passwords generated by an authenticator app.



Deriving a Verification Key:

Don't store the master password itself.
When a user creates an account, collect their master password.
Instead of storing it directly, use a Key Derivation Function (KDF) to derive two separate keys from the master password:
Encryption Key: Used to encrypt and decrypt stored passwords (as discussed earlier).
Verification Key: Used for user authentication during login attempts.


Verification Process:

During login, the user enters their master password.
The application applies the same KDF function (used during account creation) to the entered master password.
The derived verification key is compared to the stored verification key for that user.
If they match, the user is successfully authenticated.


--- sign UP   
    input (master pass)
    kdf (mp)    ->     encKey, verKey
    storeInDB(verKey)

    sign INN
    input (master pass)
    kdf (mp)    ->     encKey, verKey
    verify (verKeyDB == verKeyGenerated)
    viewPass (encDecKey)

"""