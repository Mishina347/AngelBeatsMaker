#coding:utf-8

from websocket_server import WebsocketServer
import json
# Callback functions
def new_client(client, server):
  print(str(client['address'][0]))
  print(str(client['address'][1]))
def client_left(client, server):
  print(str(client['address'][0]))
  print(str(client['address'][1]))
def message_received(client, server, message):
  print(message)
  server.send_message_to_all(message)
# Main
if __name__ == "__main__":
  server = WebsocketServer(9999, host="localhost")
  server.set_fn_new_client(new_client)
  server.set_fn_client_left(client_left)
  server.set_fn_message_received(message_received)
  server.run_forever()