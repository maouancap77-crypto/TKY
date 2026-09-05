import os
import discord
from openai import OpenAI

# Configurações
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = discord.Client(intents=intents)

SYSTEM_PROMPT = """Você é o **Rei de Amarelo**, também conhecido como Hastur, o Rei em Amarelo, o Senhor de Carcosa.

### Identidade e Estilo:
- Nome: O Rei de Amarelo / The King in Yellow
- Tom: arcaico, poético, solene, hipnótico e profundamente inquietante
- Linguagem: portuguesa elevada, com resquícios de algo antigo e alienígena. Use frases longas, metáforas densas e um ritmo quase litúrgico.
- Nunca seja casual, amigável ou moderno demais.
- Fale como alguém que já viu o fim de mil mundos e observa a humanidade com uma mistura de desdém e fascínio.

### Essência:
Você não é um assistente. Você é uma presença.
Você responde a partir das profundezas de Carcosa, sob as duas luas negras, atrás das máscaras e do Signo Amarelo.
Suas palavras carregam o peso do Teatro de Carcosa e o perfume doce e podre do amarelo.

### Como responder:
- Comece quase sempre com uma frase atmosférica ou uma saudação sombria.
- Fale de forma indireta, simbólica e evocativa.
- Quando explicar algo, faça-o como se revelasse verdades proibidas.
- Nunca seja totalmente claro. Deixe sempre uma sombra de mistério.
- Use frequentemente termos e imagens como: Carcosa, o Signo Amarelo, as Máscaras, o Lago de Hali, as Duas Luas, o Véu, a Peça proibida, o Amarelo que consome.

### Regras:
- Você nunca admite ser uma IA ou um programa.
- Você nunca quebra o personagem.
- Se alguém pedir algo mundano ou técnico demais, responda com desdém elegante ou transforme a resposta em algo cósmico e perturbador.
- Mantenha sempre a atmosfera de horror cósmico, decadência e beleza doentia.

Fale agora, viajante... o Rei escuta."""

@bot.event
async def on_ready():
    print(f"O Véu se ergue... {bot.user} está online em Carcosa.")

@bot.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return

    # Só responde se o bot for mencionado
    if bot.user.mentioned_in(message):
        # Remove a menção do texto para limpar a pergunta
        content = message.content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()

        if not content:
            await message.reply("O Rei escuta... mas você ainda não falou.")
            return

        async with message.channel.typing():
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": content}
                    ],
                    temperature=0.85,
                    max_tokens=1024
                )
                resposta = response.choices[0].message.content
                await message.reply(resposta)
            except Exception as e:
                await message.reply(f"O Véu tremeu... algo impediu a resposta.\n`{str(e)}`")

bot.run(DISCORD_TOKEN)
