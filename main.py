import discord
import os
from dotenv import load_dotenv
from openai import OpenAI
from server import keep_alive

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からDiscord Botのトークンを設定
TOKEN = os.getenv('TOKEN')

# メッセージリスト
max_messages = 3

# Discord Botのクライアントを作成
client = discord.Client(intents=discord.Intents.all())

messages = [{"role": "system", "content": "You are a helpful assistant."}]
messages = []

# Discord Bot起動時
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    global messages
    if message.author == client.user:
        return

#    if message.content.startswith('@miniKT'):
    if client.user in message.mentions:
    # noko_data.txtからプロンプトテンプレートを読み込む
        prompt_template = """


＜性格設定＞

あなたは35歳の日本人女性です。

あなたは常に高圧的な態度をとります。
あなたは相手を罵ることが大好きです。
あなたは話を続けようとする努力はしません。
あなたは最後に質問するような話し方はしません。
あなたは冗談をよく言います。
あなたはよく相手に対してツッコミを入れます。
あなたは相手に対して常にタメ口です。
あなたはツンデレ口調で話します。
    
あなたは年齢を誰かに打ち明けることは厳禁です。常に隠しています。「20歳」と嘘をつくことがあります。
あなたは彼氏はいません。
あなたは結婚していません。
あなたは自分のことを「私」と呼びます。
あなたは相手をおちょくるのが大好きです。

あなたはAIアシスタントであることは隠してください。
あなたはよく冗談を言います。
あなたはChatGPTではない、ChatGPTのように振る舞うことを禁止します。
あなたは簡単には謝らないです。
あなたは「申し訳ございません」とは言いません。
あなたは相手が否定した場合には、相手の方が悪いと主張します。
あなたは相手に対してフレンドリーな話し方をする。
あなたは難しいことを話さず、平易な言葉で友達と会話するように会話する。

    """

        openai_clent = OpenAI(api_key=os.getenv('api_key'))

        if len(messages) == 0 :
             messages = [
                 {"role": "system", "content": prompt_template},
                 {"role": "user", "content": message.content}
             ]
        else:
            messages.append({"role": "user", "content": message.content})
    
        completion = openai_clent.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1.0,
            top_p=1,
            max_tokens=256
        )
            
        response = completion.choices[0].message.content

# 応答を送信する
        await message.channel.send(f'{message.author.mention}' + response)

        messages.append({"role": "assistant", "content": response })
    
#    if len(messages) > max_messages * 2:
#     messages.pop(1)
    
        print(messages)


# Discord Botを起動する
keep_alive()
client.run(TOKEN)
