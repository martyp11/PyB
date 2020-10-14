import hashlib
user = input("Enter text here ")
h = hashlib.md5(user.encode())
h2 = h.hexdigest()
print(h2)
