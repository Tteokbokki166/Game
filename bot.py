import discord
from discord.ext import commands, tasks
from discord.ui import Select, View, Button
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="++", intents=intents)

PRIVATE_INFO_CHANNEL_ID = 1368203465125527584  # <== เปลี่ยนเป็น Channel ID ห้องข้อมูลส่วนตัวของคุณ
class InfoModal(discord.ui.Modal, title="กรอกข้อมูลรับยศ"):
    name = discord.ui.TextInput(label="ชื่อของคุณ", placeholder="ใส่ชื่อที่ต้องการ", required=True, max_length=100)
    age = discord.ui.TextInput(label="อายุของคุณ", placeholder="ใส่อายุของคุณ", required=True, max_length=3)
    gender = discord.ui.TextInput(label="เพศของคุณ", placeholder="ระบุเพศ (เช่น ชาย,หญิง,LGBTQ+,ไม่ระบุ)", required=True, max_length=20)

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user
        channel = bot.get_channel(PRIVATE_INFO_CHANNEL_ID)

        if channel:
            now = datetime.now().strftime("%#m/%#d/%Y %I:%M %p")  # ปรับรูปแบบเวลาแบบในภาพ

            embed = discord.Embed(color=discord.Color.blue())
            embed.set_author(name=str(user), icon_url=user.display_avatar.url)
            embed.set_thumbnail(url=user.display_avatar.url)

            embed.add_field(name="ชื่อ", value=self.name.value, inline=False)
            embed.add_field(name="อายุ", value=self.age.value, inline=False)
            embed.add_field(name="เพศ", value=self.gender.value, inline=False)
            embed.add_field(name="\u200b", value="‼️ ข้อมูลห้ามเผยแพร่ ‼️", inline=False)

            embed.set_footer(text=f"ID : {user.id} • {now}")

            await channel.send(embed=embed)

        await interaction.response.send_message("✅ ส่งข้อมูลเรียบร้อย! กรุณารอการอนุมัติ", ephemeral=True)

class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="แนะนำตัวตรงนี้", style=discord.ButtonStyle.success, custom_id="verify_button")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(InfoModal())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="🌃｜แนะนำตัว")
        if not channel:
            print(f"ไม่พบช่อง '🌃｜แนะนำตัว' ในเซิร์ฟเวอร์ {guild.name}")
            continue
        await setup_buttons(channel)

async def setup_buttons(channel):
    # ค้นหาข้อความที่มีปุ่มเดิม
    async for message in channel.history(limit=50):
        if message.author == channel.guild.me and message.embeds:
            if message.embeds[0].title == "รับยศ":
                print(f"พบปุ่มเดิมในแชนแนล {channel.name}")
                return

    # หากไม่มีข้อความเดิม ให้สร้างข้อความใหม่
    embed = discord.Embed(title="รับยศ", description="กดปุ่มด้านล่างเพื่อรับยศ")
    embed.set_image(url="https://media.discordapp.net/attachments/1367522884964192376/1368212396996431972/1111.jpg")

    view = VerifyButton()
    await channel.send(embed=embed, view=view)


bot.run("ODg4NDM2NjA2OTI5ODYyNjc2.GXbTca.QVC7UxuIFcJCeV3vDerbxosHOIstMC1B0AX7dk")

