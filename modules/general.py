import aiohttp
import discord
from discord.ext import commands
from utils import get, data
from lib import config
import random
import typing
import datetime
import koreanbots
import asyncio
from pytz import timezone, utc
import locale
locale.setlocale(locale.LC_ALL, '')

class General(commands.Cog, name="일반"):
    def __init__(self, miya):
        self.miya = miya

    @commands.command(name="도움말", aliases=["도움", "명령어"])
    async def _help(self, ctx):
        """
        미야야 도움말


        미야의 명령어 목록을 보여줍니다.
        """
        embed = discord.Embed(title="미야 사용법", description="< > 필드는 필수, [ ] 필드는 선택입니다. / 로 구분되어 있는 경우 하나만 선택하세요.", color=0x5FE9FF, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="도움말", icon_url=self.miya.user.avatar_url)
        for command in self.miya.commands:
            private = ["개발", "서버 데이터 관리", "PRIVATE", "경제/돈"]
            if command.cog.qualified_name in private:
                app = await self.miya.application_info()
                owner = await get.team(ctx.author.id, app)
                if owner == True:
                    temp = command.help.split("\n")[3:]
                    local = ""
                    for arg in temp:
                        local += f"{arg}\n"
                    embed.add_field(name=command.help.split("\n")[0], value=local, inline=False)
            else:
                temp = command.help.split("\n")[3:]
                local = ""
                for arg in temp:
                    local += f"{arg}\n"
                embed.add_field(name=command.help.split("\n")[0], value=local, inline=False)
        try:
            await ctx.author.send(embed=embed)
        except:
            await ctx.send(f"{ctx.author.mention} - ")
        else:
            await ctx.message.add_reaction("<:cs_sent:659355469684539402>")

    @commands.command(name="핑")
    async def ping(self, ctx):
        """
        미야야 핑


        미야의 지연 시간을 표시합니다.
        """
        channel = self.miya.get_channel(663806206376149073)
        first_time = datetime.datetime.utcnow()
        m = await channel.send("핑1")
        await m.edit(content="핑2")
        last_time = datetime.datetime.utcnow()
        await m.delete()
        ocha = str(last_time - first_time)[6:]
        row = await data.load("miya", "botId", self.miya.user.id)
        record = str(row[1].split(".")[0])
        start_time = datetime.datetime.strptime(record, "%Y-%m-%d %H:%M:%S")
        uptime = datetime.datetime.utcnow() - start_time
        embed = discord.Embed(color=0x5FE9FF, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="API 지연 시간", value=f"{round(self.miya.latency * 1000)}ms", inline=False)
        embed.add_field(name="메시지 수정 오차", value=f"{round(float(ocha) * 1000)}ms", inline=False)
        embed.add_field(name="구동 시간", value=str(uptime).split(".")[0])
        embed.set_thumbnail(url=ctx.author.avatar_url_as(static_format="png", size=2048))
        embed.set_author(name="지연 시간", icon_url=self.miya.user.avatar_url)
        await ctx.send(f":ping_pong: {ctx.author.mention} Pong!", embed=embed)

    @commands.command(name="초대")
    async def _invite(self, ctx):
        """
        미야야 초대


        미야의 초대 링크를 표시합니다.
        """
        embed = discord.Embed(title="미야 초대링크", description="[여기](https://discord.com/api/oauth2/authorize?client_id=720724942873821316&permissions=2147483647&redirect_uri=http%3A%2F%2Fmiya.kro.kr&response_type=code&scope=bot%20identify%20email)를 클릭하면 초대하실 수 있어요!", color=0x5FE9FF, timestamp=datetime.datetime.utcnow())
        await ctx.send(ctx.author.mention, embed=embed)
    
    @commands.command(name="피드백", aliases=["문의", "지원"])
    async def request(self, ctx, *, message):
        """
        미야야 문의 < 할말 >


        미야 관리팀에게 문의 메세지를 전송합니다.
        """
        channel = self.miya.get_channel(config.Newsfeed)
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        embed = discord.Embed(title="피드백이 도착했어요!", color=0x95E1F4)
        embed.add_field(name="피드백을 접수한 유저", value=f"{ctx.author} ( {ctx.author.id} )", inline=False)
        embed.add_field(name="피드백이 접수된 서버", value=f"{ctx.guild.name} ( {ctx.guild.id} )", inline=False)
        embed.add_field(name="피드백이 접수된 채널", value=f"{ctx.channel.name} ( {ctx.channel.id} )", inline=False)
        embed.add_field(name="피드백 내용", value=message, inline=False)
        embed.add_field(name="피드백 접수 완료 시간", value=time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초"), inline=False)
        embed.set_author(name="문의 및 답변", icon_url=self.miya.user.avatar_url)
        msg = await ctx.send(f"{ctx.author.mention} 이렇게 전송하는 게 맞나요?\n```{message}```")
        await msg.add_reaction("<:cs_yes:659355468715786262>")
        await msg.add_reaction("<:cs_no:659355468816187405>")
        def check(reaction, user):
            return reaction.message.id == msg.id and user == ctx.author
        try:
            reaction, user = await self.miya.wait_for('reaction_add', timeout=60, check=check)
        except asyncio.TimeoutError:
            await msg.delete()
        else:
            if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                await msg.edit(content=f"<:cs_yes:659355468715786262> {ctx.author.mention} 개발자에게 전송했어요! 피드백 명령어를 용도에 맞게 사용하지 않거나 이유 없이 사용하시면 봇 사용이 제한될 수 있어요.", embed=None, supress=True, delete_after=10)
                await channel.send("@everyone", embed=embed)
            else:
                await msg.delete()

    @commands.command(name="봇정보", aliases=["미야정보", "미야"])
    async def _miyainfo(self, ctx):
        """
        미야야 미야


        미야의 정보를 표시합니다.
        """
        working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
        heart = await self.miya.get_rank()
        e = discord.Embed(title="미야 서버(봇) 정보",
            description=f"""
                <:koreanbots:752354740314177568> 봇 순위 : {heart}위 [하트 누르기](https://koreanbots.dev/bots/720724942873821316)
                <:GitHub_W:782076841141207071> 코드 저장소 : [보러 가기](https://github.com/LRACT/Miya)
                <:cs_settings:659355468992610304> 호스트 : 개인 서버 - 한국
                <:cs_on:659355468682231810> 리라이트 시작 : 2020년 8월 17일
                <:cs_leave:659355468803866624> 서버 수 : {len(self.miya.guilds)}개""", color=0x5FE9FF, timestamp=datetime.datetime.utcnow())
        e.set_thumbnail(url=self.miya.user.avatar_url_as(static_format='png', size=2048))
        e.set_author(name="정보", icon_url=self.miya.user.avatar_url)
        await working.edit(content=ctx.author.mention, embed=e)

    @commands.command(name="한강")
    async def _hangang(self, ctx):
        """
        미야야 한강


        현재 한강의 수온을 출력합니다.
        """
        working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://hangang.dkserver.wo.tc") as r:
                response = await r.json(content_type=None)
                embed = discord.Embed(description=f'현재 한강의 온도는 `{response["temp"]}`도에요!\n`측정: {(response["time"]).split(" ")[0]}`', color=0x5FE9FF)
                embed.set_author(name="지금 한강은", icon_url=self.miya.user.avatar_url)
                temp = None
                if "." in response["temp"]:
                    temp = int(response["temp"].split(".")[0])
                else:
                    temp = int(response["temp"])

                if temp > 15:
                    embed.set_footer(text="거 수온이 뜨듯하구먼!")
                else:
                    embed.set_footer(text="거 이거 완전 얼음장이구먼!")
                await working.edit(content=ctx.author.mention, embed=embed)

    @commands.command(name="골라", aliases=["골라줘"])
    async def _select(self, ctx, *args):
        """
        미야야 골라 < 단어 1 > < 단어 2 > [ 단어 3 ] ...


        미야가 단어 중 랜덤하게 하나를 선택해줍니다.
        """
        if not args or len(args) <= 1:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 골라 < 단어 1 > < 단어 2 > [ 단어 3 ] ...`이 올바른 명령어에요!")
        else:
            select = random.choice(args)
            embed = discord.Embed(description=select, color=0x5FE9FF)
            embed.set_author(name="미야의 선택은...", icon_url=self.miya.user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name="프로필", aliases=["프사", "프로필사진", '아바타'])
    async def _profile(self, ctx, user: typing.Optional[discord.User] = None):
        """
        미야야 프로필 [ @유저 ]


        지목한 유저의 프로필을 보여줍니다.
        지목이 되지 않았을 경우 자신의 프로필을 보여줍니다.
        """
        if user is None:
            user = ctx.author
        embed = discord.Embed(color=0x5FE9FF)
        embed.set_author(name=f"{user.name}님의 프로필 사진", icon_url=self.miya.user.avatar_url)
        embed.set_image(url=user.avatar_url_as(static_format="png", size=2048))
        await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(name="서버정보")
    async def _serverinfo(self, ctx):
        """
        미야야 서버정보


        명령어를 실행한 서버의 정보와 미야 설정을 불러옵니다.
        """
        working = await ctx.send(
            f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!"
        )
        embed = discord.Embed(title=f"{ctx.guild.name} 정보 및 미야 설정", color=0x5FE9FF)
        guilds = await data.load("guilds", "guild", ctx.guild.id)
        memberNoti = await data.load("memberNoti", "guild", ctx.guild.id)
        muteRole = "설정되어 있지 않아요!"
        memberCh = "설정되어 있지 않아요!"
        logCh = "설정되어 있지 않아요!"
        if guilds[2] != 1234:
            role = ctx.guild.get_role(int(guilds[2]))
            if role is not None:
                muteRole = role.mention
        if memberNoti[1] != 1234:
            channel = ctx.guild.get_channel(int(memberNoti[1]))
            if channel is not None:
                memberCh = channel.mention
        if guilds[1] != 1234:
            channel = ctx.guild.get_channel(int(guilds[1]))
            if channel is not None:
                logCh = channel.mention
        location = {
            "amsterdam": "네덜란드 - 암스테르담",
            "brazil": "브라질",
            "dubai": "아랍에미리트 - 두바이",
            "eu_central": "유럽 - 중부",
            "eu_west": "유럽 - 서부",
            "europe": "유럽",
            "frankfurt": "독일 - 프랑크푸르트",
            "hongkong": "홍콩",
            "india": "인도",
            "japan": "일본",
            "london": "영국 - 런던",
            "russia": "러시아",
            "singapore": "싱가포르",
            "southafrica": "남아프리카",
            "south-korea": "대한민국",
            "sydney": "호주 - 시드니",
            "us-central": "미국 - 중부",
            "us-east": "미국 - 동부",
            "us-south": "미국 - 남부",
            "us-west": "미국 - 서부",
            "vip-amsterdam": "<:vip:762569445427511307> 네덜란드 - 암스테르담",
            "vip-us-east": "<:vip:762569445427511307> 미국 - 동부",
            "vip-us-west": "<:vip:762569445427511307> 미국 - 서부"
        }
        verification = {
            discord.VerificationLevel.none: "**없음**\n제한 없음",
            discord.VerificationLevel.low: "**낮음**\n이메일 인증이 완료된 Discord 계정이어야 해요.",
            discord.VerificationLevel.medium: "**중간**\n이메일 인증이 완료되고, Discord에 가입한 지 5분이 지나야 해요.",
            discord.VerificationLevel.high: "**높음**\n이메일 인증이 완료되고, Discord에 가입한 지 5분이 지나며, 서버의 멤버가 된 지 10분이 지나야 해요.",
            discord.VerificationLevel.extreme: "**매우 높음**\n휴대폰 인증이 완료된 Discord 계정이어야 해요."
        }
        KST = timezone('Asia/Seoul')
        now = ctx.guild.created_at
        time = utc.localize(now).astimezone(KST)
        embed.add_field(name="공지 채널", value="📢 **서버의 연동 설정을 확인하세요!**", inline=False)
        embed.add_field(name="멤버 알림 채널", value=memberCh)
        embed.add_field(name="로그 채널 ⚒️", value=logCh)
        embed.add_field(name="뮤트 역할", value=muteRole)
        embed.add_field(name="서버 부스트 인원 수", value=f"{len(ctx.guild.premium_subscribers)}명")
        embed.add_field(name="서버 오너", value=f"{str(ctx.guild.owner)}님")
        embed.add_field(name="서버 인원 수", value=f"{ctx.guild.member_count}명")
        embed.add_field(name="서버 역할 갯수", value=f"{len(ctx.guild.roles)}개")
        embed.add_field(name="서버 위치", value=location[str(ctx.guild.region)])
        embed.add_field(name="서버 개설 날짜", value=time.strftime("%Y년 %m월 %d일"))
        embed.add_field(name="서버 보안 수준", value=verification[ctx.guild.verification_level])
        embed.set_author(name="정보", icon_url=self.miya.user.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png", size=2048))
        await working.edit(content=ctx.author.mention, embed=embed)

    @commands.command(name="말해", aliases=["말해줘"])
    @commands.bot_has_permissions(manage_messages=True)
    async def _say(self, ctx, *args):
        """
        미야야 말해 < 할말 >


        미야가 당신이 한 말을 조금 가공해서(?) 따라합니다.
        """
        if not args:
            await ctx.send(f"{ctx.author.mention} `미야야 말해 < 할말 > ` 이 올바른 명령어에요!")
        else:
            text = " ".join(args)
            embed = discord.Embed(description=text, color=0x5FE9FF)
            embed.set_author(name=f"{ctx.author}님이 말하시길...", icon_url=ctx.author.avatar_url)
            await ctx.message.delete()
            await ctx.send(embed=embed)

    @commands.command(name="코로나")
    async def _corona_info(self, ctx):
        """
        미야야 코로나


        대한민국의 코로나 현황을 불러옵니다.
        """
        working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
        _corona = await get.corona()
        embed = discord.Embed(title="국내 코로나19 현황", description="질병관리청 집계 기준", color=0x5FE9FF)
        embed.add_field(name="확진자", value=f"{_corona[0].split(')')[1]}명", inline=True)
        embed.add_field(name="완치(격리 해제)", value=f"{_corona[1]}명", inline=True)
        embed.add_field(name="치료 중", value=f"{_corona[2]}명", inline=True)
        embed.add_field(name="사망", value=f"{_corona[3]}명", inline=True)
        embed.add_field(name="정보 출처", value="[질병관리청](http://ncov.mohw.go.kr/)", inline=True)
        embed.set_author(name="COVID-19", icon_url=self.miya.user.avatar_url)
        embed.set_footer(text="코로나19 감염이 의심되면 즉시 보건소 및 콜센터(전화1339)로 신고바랍니다.")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/746786600037384203/761404488023408640/unknown.png") 
        await working.edit(content=f"{ctx.author.mention} 현재 코로나19 현황이에요!", embed=embed)

    @commands.command(name="하트")
    async def _vote(self, ctx, user: typing.Optional[discord.User] = None):
        """
        미야야 하트 [ @유저 ]


        한국 디스코드 봇 리스트의 미야에게 하트를 눌러주셨는지 확인합니다.
        """
        if user is None:
            user = ctx.author
        working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
        try:
            response = await self.miya.koreanbots.getVote(user.id)
        except koreanbots.NotFound:
            await working.edit(content=f":broken_heart: {ctx.author.mention} **{user}**님은 미야에게 하트를 눌러주지 않으셨어요...\n하트 누르기 : https://koreanbots.dev/bots/720724942873821316")
        else:
            if response.voted:
                await working.edit(content=f":heart: {ctx.author.mention} **{user}**님은 미야에게 하트를 눌러주셨어요!\n하트 누르기 : https://koreanbots.dev/bots/720724942873821316")
            else:
                await working.edit(content=f":broken_heart: {ctx.author.mention} **{user}**님은 미야에게 하트를 눌러주지 않으셨어요...\n하트 누르기 : https://koreanbots.dev/bots/720724942873821316")

    @commands.command(name="오리", aliases=['랜덤오리'])
    async def _duck(self, ctx):
        """
        미야야 오리


        랜덤으로 아무 오리 사진이나 가져옵니다.
        """
        working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
        async with aiohttp.ClientSession() as session:
            async with session.get("https://random-d.uk/api/v2/quack") as response:
                p = await response.json()
                duck = discord.Embed(color=0xFFFCC9, timestamp=datetime.datetime.utcnow())
                duck.set_image(url=p['url'])
                duck.set_author(name="어떠한 오리 사진에 대하여", icon_url=self.miya.user.avatar_url)
                duck.set_footer(text=p['message'])
                await working.edit(content=ctx.author.mention, embed=duck)

def setup(miya):
    miya.add_cog(General(miya))
