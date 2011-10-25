# -*- coding: utf-8 -*-

import socket
from urllib import urlopen
import weather

class IrcBot():
    def __init__(self,host,port,nick):
        self.host = host
        self.port = port
        self.nick = nick
        self.channels = []
        self.commands = {"sää":self.c_weather}
        self.sock = None
        self.admins = ["namochan@5w.fi","namochan@namochan.tontut.fi"]
        self.running = True
        self.messages = {"namochan":"<namo> Muista ostaa maitoa!"}

    def connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.host,self.port))
        self.send("NICK "+self.nick)
        self.send("USER PyBot namochan.com Hum PythonBot")

    def join(self,chan):
        self.channels.append(chan)
        self.send("JOIN "+chan)

    def send(self,msg):
        self.sock.send(msg+"\n\r")

    def say(self,data,channel):
        print ( ( "%s: %s") % (self.nick, data) )
        self.sock.send( (("PRIVMSG %s :%s\r\n") % (channel, data)))

    def run(self):
        while True:
            line = self.sock.recv(4096)
            print(line)
            if line == '':
                return

            if line.split()[0]=='PING':
                self.send('PONG '+line[1])
            if len(line.split()) > 3:
                if line.find('PRIVMSG')>=0:
                    line=line.rstrip()
                    self.parse(line)

    def quit(self):
        self.sock.close()
        
    def parse(self,msg):
        complete = msg[1:].split(':',1)
        info=complete[0].split(' ')
        msgpart=complete[1]
        sender=info[0].split('!')
        if len(sender) < 2:
            return
        if sender[1] not in self.admins:
            print("<"+sender[0]+"> "+msgpart)
            return
        print("<@"+sender[0]+"> "+msgpart)
        if msgpart.startswith("!"):
            msgpart = msgpart[1:]
            cmd = msgpart.split()[0]
            if self.commands.has_key(cmd):
                self.commands[cmd](msgpart,sender[0],info[2])

    def c_weather(self,data,sender,channel):
        city = "Tampere"
        if len(data.split(" ",1)) > 1:
            city = data.split(" ",1)[1]
            city = city.title()
        w = weather.getWeather(city)
        if w is not None:
            self.say(w,channel)
        else:
            self.say("Can't get weather, sorry.",channel)

    def c_leavemessage(self):
        pass

def main():
    irc = IrcBot("irc.freenode.net",6667,"namobot")
    print("Connecting...")
    irc.connect()
    print("Connected.")
    irc.join("#5wbot")
    irc.run()

if __name__ == "__main__":
    main()
