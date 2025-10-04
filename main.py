from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger # 使用 astrbot 提供的 logger 接口
import astrbot.api.message_components as Comp
from astrbot.api import AstrBotConfig
import aiohttp
from xpinyin import Pinyin
import re
from selenium import webdriver
from PIL import Image


@register("astrbot_plugin_radar", "M42", "获取城市雷达图", "1.0", "https://github.com/XCM42-Orion/astrbot_plugin_radar")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def fetch(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
        

    @filter.command("radar")
    async def get_radar(self, event: AstrMessageEvent):
        '''获取城市雷达信息''' 
        async with aiohttp.ClientSession() as session:
            user_name = event.get_sender_name()
            message_str = event.message_str
            logger.info(f"{user_name}尝试获取雷达信息......")
            try:
                province = message_str.split()[1]
                city = message_str.split()[2]
            except IndexError:
                yield event.plain_result("参数错误，请输入省份与城市（例：/radar 山东 烟台）")
            else:
                url = f'https://www.nmc.cn/publish/radar/{Pinyin().get_pinyin(province)}/{Pinyin().get_pinyin(city)}.htm'
                response = await MyPlugin.fetch(url)
                title = re.search('<title>中央气象台-404错误页面</title>',response)
                if title == None:
# 配置浏览器选项
                    option = webdriver.ChromeOptions()
                    option.add_argument('headless') # 无头模式，不显示浏览器窗口

# 创建浏览器驱动
                    driver = webdriver.Chrome(options=option)
# 打开网页
                    driver.get(url)
# 获取网页的宽度和高度
                    width = driver.execute_script("return document.documentElement.scrollWidth")
                    height = driver.execute_script("return document.documentElement.scrollHeight")
# 设置浏览器窗口大小以适应整个网页
                    driver.set_window_size(width, height)
# 截取整个网页并保存为文件
                    driver.get_screenshot_as_file('webpage.png')
                    image = Image.open("webpage.png")
                    left = 235
                    top = 400
                    right = 1043
                    bottom = 1043
                    cropped_image = image.crop((left, top, right, bottom))
                    cropped_image.save("cropped_element.png")
                    chain = [
                            Comp.Plain(f"已获取{province},{city}的雷达信息："),
                            Comp.Image.fromFileSystem("cropped_element.png")
                            ]
                    yield event.chain_result(chain)
                    driver.quit()
                else:
                    yield event.plain_result("页面不存在，请检查雷达站是否存在或输入有无错误......")


