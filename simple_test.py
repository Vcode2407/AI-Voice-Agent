import asyncio
import websockets
import json

async def simple_test():
    uri = "ws://localhost:3000/ws"
    
    print("Connecting to agent...")
    async with websockets.connect(uri) as websocket:
        print("Connected! Waiting for agent messages...")
        
        # Just listen to what the agent sends
        try:
            async for message in websocket:
                data = json.loads(message)
                msg_type = data.get("type", "unknown")
                print(f"\n[{msg_type}]")
                
                # Show important messages
                if msg_type == "response.audio_transcript.delta":
                    print(f"Agent speaking: {data.get('delta', '')}")
                elif msg_type == "response.text.delta":
                    print(f"Agent text: {data.get('delta', '')}")
                elif msg_type == "response.function_call_arguments.delta":
                    print(f"Tool call: {data.get('delta', '')}")
                elif msg_type == "error":
                    print(f"ERROR: {data}")
                    break
                
                # Print full message for debugging
                print(json.dumps(data, indent=2))
                
        except KeyboardInterrupt:
            print("\nStopped by user")

asyncio.run(simple_test())
