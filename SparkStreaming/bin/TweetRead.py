#import ./config
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json

consumer_key="fzehcL8ijXVZQOnxEUSztojmg"
consumer_secret="DDd6j8HEPiFiXLexUe841mTVYOiAMncjsFWZ6i5ed2LoGH5tmb"
access_token="169852890-7HplGdHvDSUPqh4gKkLCxf1d422xPneiAS8U3EZU"
access_secret="iXzssw04wqawGbHh49n3ufQJtSJAe5HlGogt4EvKMofh9"


class TweetsListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket

    def on_data(self, data):
        try:
            msg = json.loads(data)
            print(msg['text'].encode('utf-8'))
            self.client_socket.send(msg['text'].encode('utf-8'))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


def sendData(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, TweetsListener(c_socket))
    # filter just nyc
    # twitter_stream.filter(locations=[-74,40,-73,41])
    twitter_stream.filter(track=['trump'])


if __name__ == "__main__":
    s = socket.socket()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    host = (sock.getsockname()[0])
    sock.close()  # Get IP.
    print("Host is:", host)
    port = 5555  # Reserve a port.
    s.bind((host, port))  # Bind to the port

    print("Listening on port: %s" % str(port))

    s.listen(5)  # Now wait for client connection.
    c, addr = s.accept()  # Establish connection with client.

    print("Received request from: " + str(addr))

    sendData(c)
