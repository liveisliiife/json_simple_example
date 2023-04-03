import os
import json

class User:
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    def intro(self):
        print(f"Name: {self.username}   and   email: {self.email}")



class UserRepository:
    def __init__(self):
        self.users = []   # uygulama çalışınca burayı userları depolamak için kullanacaz. Eger json dosyası varsa
                          # ordaki bilgileri ilk başta buna ekleyecez.
        self.isLoggedIn = False  # kullinici daha önce giris yapmış mı yapmamış mı buna bakmak için
        self.currentUser = {}   # eğer kullanici login olmuşsa bilgileri buraya aktarılacak

        # load users from .json file ---> varolan tüm kullanici bilgilerini users listesine aktaracaz
        self.loadUsers()

    # dosya okuma işlemi yapacaz. Tüm userları users listesine atacaz
    # dosya ilk başta kullanılıyorsa olmayacak bu yüzden os import edildi
    def loadUsers(self):
        if os.path.exists("users.json"): # bu isimde bir dosya bu path'de var mı diye bakiyor
            with open("users.json","r",encoding="utf-8") as file:
                coming_from_file_users = json.load(file)
                print(coming_from_file_users)   # kayıtlı kullanicilar
                for currentUser in coming_from_file_users:
                    currentUser = json.loads(currentUser)

                    new_user = User(username=currentUser["username"],password=currentUser["password"],email=currentUser["email"])
                    self.users.append(new_user)


            print(self.users)


    # kullanıcı oluşturma
    def register(self,user:User):
        self.users.append(user)     #users listesine gönderilen kullanici ekleniyor
        self.savetoFile()   # register ile kullanici olusturulunca bu kullaniciyi json dosyaya kaydetmek için
        print("Kullanici olusturuldu")


    #kullanıcı girişi
    def login(self,username,password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.isLoggedIn = True  # kullanıcı sisteme girdi
                self.currentUser = user
                print("Login yapildi")
                break

    def logout(self):
        self.isLoggedIn = False
        self.currentUser = {}
        print("Çıkış yapildi")

    def identity(self):
        if self.isLoggedIn == True:
            print("Kisisel Bilgileriniz...")
            self.currentUser.intro()

        else:
            print("Giris yapilmadi")

    # bilgileri json bilgisi olarak alıp database'a kaydedecek
    def savetoFile(self):
        temp_list = [] # bu liste users listesindeki class olan elemanları dicte çevrildiklerinde tutacak olan liste

        for temp_user in self.users:
            temp_list.append(json.dumps(temp_user.__dict__))

        with open("users.json","w") as file:
            json.dump(temp_list,file)  # her birisi dict elemanlardan oluşan temp_list objesini json file'a kaydedecek.


my_repistory = UserRepository()

while True:
    print("Menü".center(50,"*"))
    secim = input("1- Register(Kaydol)\n2- Login(Giris)\n3- Logout(Kullanici cikisi yapmak icin)\n4- Identity(O anda kim login)\n5- Exit(Programdan cikmak icin)\nSeciminiz: ")

    if secim == "5":
        break
    elif secim == "1":
        kullanici_adi = input("Username:")
        kullanici_password = input("Password:")
        kullanici_email = input("email:")

        new_user = User(username=kullanici_adi,password=kullanici_password,email=kullanici_email)

        my_repistory.register(new_user)

        print("Sistemde kayıtlı olan tüm kullanicilar: ",my_repistory.users)

    elif secim == "2":
        if my_repistory.isLoggedIn == True:
            print("Zaten login oldunuz...")
        else:
            kullanici_adi = input("Username:")
            kullanici_password = input("Password:")
            my_repistory.login(kullanici_adi,kullanici_password)

    elif secim == "3":
        my_repistory.logout()

    elif secim == "4":
        my_repistory.identity()

    else:
        print("Hatali tusa bastiniz")
