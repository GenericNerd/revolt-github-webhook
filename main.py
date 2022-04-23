import pyrevolt
from flask import Flask, request
import os
import json

app: Flask = Flask(__name__)


@app.route("/payload", methods=["POST"])
async def payload():
    data: dict = request.get_json(force=True)
    commits: str = ""
    for commit in data["commits"]:
        commits += f"[{commit['id'][0:8]}]({commit['url']}) - {commit['message']}\n"
    embed: pyrevolt.Embed = pyrevolt.Embed.Create(title=data['repository']['full_name'], url=data['repository']['html_url'], description=commits)
    client: pyrevolt.HTTPClient = pyrevolt.HTTPClient()
    revoltRequest: pyrevolt.Request = pyrevolt.Request(pyrevolt.Method.POST, f"/channels/{os.getenv('CHANNEL_ID')}/messages", data={"content": "<200b>", "embeds": [json.loads(embed.toJSON())]})
    revoltRequest.AddAuthentication(os.getenv("TOKEN"))
    await client.Request(revoltRequest)
    await client.Close()
    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0")