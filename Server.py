#!/usr/bin/python

# modules inmport
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json, sqlite3



# specify the port
PORT_NUMBER = 8000

# Set up DB connection
db = sqlite3.connect('example.db')       
db.execute("""CREATE TABLE if not exists login (email, password)""")
db.execute("""CREATE TABLE if not exists userinfo (gender, height, weight, basketballStyle, favorableBasketballCourt, availableTime, position)""")

cur = db.cursor()

login_command="""SELECT email, password FROM login"""

signup_command = "INSERT INTO login (email, password) VALUES (?, ?)"

user_info = "INSERT INTO userinfo(gender, height, weight, basketballStyle, favorableBasketballCourt, availableTime, position) VALUES (?, ?, ?, ?, ?, ?, ?)"

#This class will handles the post requests (sign in and up) from

class myHandler(BaseHTTPRequestHandler):    

    #Handler for the POST requests
    def do_POST(self):

        '''
                          ***** This is for the Login  *****
        '''
        if self.path.endswith("/login/"):



            loginList = (self.rfile.read(int(self.headers['Content-Length'])))

            email_login = self.headers['email']
            password_login = self.headers['passcode']

            cur.execute(login_command)

            loginTable = list(cur)
            t = 0

            try:
                for i, j in loginTable:

                    if i == email_login and j == password_login:
                        t = t + 1
                        print("Welcome ===> ",email_login, password_login, "\n\n")
                        #return self.wfile.write("200");
                        self.send_response(200)
                if t == 0:
                        print("Invalid account ===> ",email_login, password_login, "\n\n")
                        self.send_response(400)
                self.send_header('Content-type','text/html')
                self.end_headers()

            except sqlite3.IntegrityError:
                print("something is wrong =-=-=-=-=-=-=-> ?? ")
            return



        '''
                          ***** This is for the signup  *****
        '''
        
        if self.path.endswith("/signup/"):

            signupList = (self.rfile.read(int(self.headers['Content-Length'])))
            usernameSignup = self.headers['email']
            passwordSignup = self.headers['passcode']

            try:
                cur.execute(signup_command,(usernameSignup, passwordSignup))

                db.commit()
                self.send_response(200)

                print("\n\nuser== >", usernameSignup, "\npassword == >",passwordSignup)
                
            except sqlite3.IntegrityError:
                self.send_response(400)


            self.send_header('Content-type','text/html')
            self.end_headers()

            return

        '''
                  ***** This is for the userinfo  *****
        '''

        if self.path.endswith("/userinfo/"):

            userinfoList = (self.rfile.read(int(self.headers['Content-Length'])))

            genderInfo = self.headers['gender']
            heightInfo = self.headers['height']
            weightInfo = self.headers['weight']
            basketballStyleInfo = self.headers['basketballStyle']
            favorableBasketballCourtInfo = self.headers['favorableBasketballCourt']
            availableTimeInfo = self.headers['availableTime']
            positionInfo = self.headers['position']

            try:
                cur.execute(user_info, (genderInfo, heightInfo, weightInfo, basketballStyleInfo, favorableBasketballCourtInfo, availableTimeInfo, positionInfo))

                db.commit()
                self.send_response(200)

                print("\n gender== >", genderInfo, "\n height == >",heightInfo, "\n weight == >",weightInfo, "\n basketballStyle== >",basketballStyleInfo,
                      "\n favorableBasketballCourt == >",favorableBasketballCourtInfo, "\n availableTime == >",availableTimeInfo, "\n position == >",positionInfo)

            except sqlite3.IntegrityError:
                self.send_response(400)

            self.send_header('Content-type','text/html')
            self.end_headers()

            return




    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write("'REQUEST_METHOD':'GET'")
        self.wfile.write("\n\n")
        self.wfile.write("Server is done.")
        return

if __name__ == '__main__':
        '''
        =====================================================================
                         *****  Run the stuff here  *****
        =====================================================================
        '''
        try:
                #Create a web server and define the handler to manage the
                #incoming request
                print ('\n\nServer is taking off ...')

                server = HTTPServer(('', PORT_NUMBER), myHandler)

                print ('\n\n Server is running on port => (__' , PORT_NUMBER, '__) <=\n\n')

                #Wait forever for incoming htto requests
                server.serve_forever()

        except KeyboardInterrupt:
                print ('\n\n\n===> ^C <=== Detected, shutting down the server\n')
                server.socket.close()


