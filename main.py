import pyrevolt
from flask import Flask, request
import os

app: Flask = Flask(__name__)

@app.route("/payload", methods=["POST"])
async def payload():
    data: dict = request.json
    commits: str = ""
    for commit in data["commits"]:
        commits += f"`[{commit['id'][0:8]}]({commit['url']})` - {commit['message']}\n"
    embed: pyrevolt.Embed = pyrevolt.Embed.Create(title=f"[{data['repository']['full_name']}]({data['repository']['html_url']})", description=commits)
    client: pyrevolt.HTTPClient = pyrevolt.HTTPClient()
    revoltRequest: pyrevolt.Request = pyrevolt.Request(pyrevolt.Method.GET, f"/channels/{os.getenv('CHANNEL_ID')}/messages", data={"content": "​", "embeds": [embed.toJSON()]})
    revoltRequest.AddAuthentication(os.getenv("TOKEN"))
    await client.Request(revoltRequest)
    await client.Close()
    return "", 200

app.run()