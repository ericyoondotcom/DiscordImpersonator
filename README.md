# DiscordImpersonator
A bot that generates new messages impersonating another user, based on their past message history (with Markov chains)!

## Getting Started
- Create an activate a venv!
- Install dependencies: `pip3 install -r requirements.txt`
- Make a copy of `config-TEMPLATE.py` as `config.py`, and paste your Discord bot token, along with the ids of all of the channels to download as training data.
- Run the bot: `python3 main.py`
- Download the training data by issuing the bot command `sus download` (you only need to do this once)
    - Downloaded channels are saved in `data/channels/the_channel_id`
- Once data is downloaded, use `sus run @mentioned_user` to impersonate the user!
    - Note: the first time the algorithm is run on a user, a model will be created and cached in `data/models/the_user_id`

> Note: every user's model is trained on all channels in `data/channels` when it is first generated. If you're running the bot in multiple guilds, delete channels that are not in the guild you want to use otherwise the bot may leak sensitive info.