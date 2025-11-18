import os
import pandas as pd
import yaml
from telethon import TelegramClient
import re
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

api_id = config["telegram"]['api_id']
api_hash = config["telegram"]['api_hash']

target_entity = "https://t.me/xinqun"


async def get_entity_chat(client, entity):
    entity = await client.get_entity(entity)

    telegram_data = {
        "message_id": [],
        "date": [],
        "sender_id": [],
        "sender_name": [],
        "text": []
    }

    async for msg in client.iter_messages(entity=entity, limit=None):
        msg_id = msg.id
        msg_date = msg.date
        sender_id = None
        sender_name = None

        if msg.sender:
            sender_id = msg.sender_id
            # first_name / last_name / username 등을 조합
            if getattr(msg.sender, "first_name", None) or getattr(msg.sender, "last_name", None):
                first = getattr(msg.sender, "first_name", "") or ""
                last = getattr(msg.sender, "last_name", "") or ""
                sender_name = (first + " " + last).strip()
            else:
                sender_name = getattr(msg.sender, "username", None)

        text = msg.message or ""
        telegram_data["message_id"].append(msg_id)
        telegram_data["date"].append(msg_date)
        telegram_data["sender_id"].append(sender_id)
        telegram_data["sender_name"].append(sender_name)
        telegram_data["text"].append(text)

    return telegram_data


with TelegramClient(f"telegram_session", api_id, api_hash) as client:
    x = client.loop.run_until_complete(get_entity_chat(client, target_entity))

# %%
df = pd.DataFrame(x)

# %%
# with TelegramClient(f"telegram_session", api_id, api_hash) as client:
#     y = client.loop.run_until_complete(get_entity_chat(client, "https://t.me/+V1xs8Ht67Ec2MTcx"))
#%%
with TelegramClient(f"telegram_session", api_id, api_hash) as client:
    # client.loop.run_until_complete(
    #     client(ImportChatInviteRequest("V1xs8Ht67Ec2MTcx"))
    # )
    y = client.loop.run_until_complete(get_entity_chat(client, "https://t.me/+V1xs8Ht67Ec2MTcx"))
#%%
df2 = pd.DataFrame(y)
#%%
pattern = r'(?:https?://)?t\.me/(?:\+|joinchat/)([A-Za-z0-9_-]+)'
def parse_group_id(text):
    matches = re.findall(pattern, text)
    return matches
#%%
df["g_ids"] = df.text.apply(parse_group_id)





#%%

