import asyncio
import websockets

async def response(websocket, path):
        ## Wait to receive a message from the client
        message = await websocket.recv()
        print(f"Received message: {message}.")
        ## Send a response back to the client
        msg = input()
        await websocket.send(msg)

## Start the server and run forever
start_server = websockets.serve(response, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
