import asyncio
import websockets
import json

async def send_and_receive():
    uri = "ws://localhost:3000/ws"
    
    print("Connecting to agent...")
    async with websockets.connect(uri) as websocket:
        print("Connected!")
        
        # Send a session update to start conversation
        session_update = {
            "type": "session.update",
            "session": {
                "modalities": ["text"],
                "instructions": "Speak only in Telugu. Help user find government schemes.",
            }
        }
        await websocket.send(json.dumps(session_update))
        print("Sent session update")
        
        # Wait a bit
        await asyncio.sleep(1)
        
        # Send user message
        user_message = {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [{
                    "type": "input_text",
                    "text": "నాకు 25 సంవత్సరాలు. నేను రైతును."
                }]
            }
        }
        await websocket.send(json.dumps(user_message))
        print("Sent user message")
        
        # Request response
        await websocket.send(json.dumps({"type": "response.create"}))
        print("Requested response\n")
        
        # Listen for responses
        try:
            async for message in websocket:
                data = json.loads(message)
                msg_type = data.get("type", "")
                
                if "text.delta" in msg_type:
                    print(data.get("delta", ""), end="", flush=True)
                elif "text.done" in msg_type:
                    print("\n")
                elif "response.done" in msg_type:
                    print("\n[Response complete]")
                    break
                elif "error" in msg_type:
                    print(f"\nERROR: {data}")
                    break
                    
        except KeyboardInterrupt:
            print("\nStopped")

asyncio.run(send_and_receive())
