from toolbox_langchain import ToolboxClient
import nest_asyncio
import asyncio

nest_asyncio.apply()

class GoogleMCPtoolbox:

    def __init__(self):
        self.tools = None

    async def load_redis_tools(self):
        async with ToolboxClient("http://127.0.0.1:5000") as client:
            self.tools = await client.aload_toolset()

            
async def main():
    toolbox = GoogleMCPtoolbox()
    await toolbox.load_redis_tools()
    for tool in toolbox.tools:
        print(tool)

if __name__ == "__main__":
    asyncio.run(main())    