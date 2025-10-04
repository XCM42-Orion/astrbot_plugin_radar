# astrbot_plugin_radar

v1.0 by M42

Astrbot插件，获取全国实时雷达图。

## 使用方法

` /radar <省份> <雷达站名> `可以获取该雷达站的实时雷达图。

例：` /radar 江苏 徐州 `

## 依赖

selenium，PIL

## Todo list

1.目前的逻辑是用selenium获取网页截图。我会找一下有没有更好更普适的办法（如果没有至少也要用playwright改成异步的）。

2.因为没有找到雷达站直接对应的省份所以目前必须要输入省份+雷达站名，以后会尝试解决这个问题
