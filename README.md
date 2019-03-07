# baidu_translate
百度翻译接口爬虫（js解密sign）

### 程序介绍
直接启动接入百度翻译接口

输入“q”后回车退出程序

### 项目技术
js解密sign参数： 通过execjs加载网页js加密sign参数相关代码，提取sign参数值。

cookie：  该接口有cookie加密，加密参数Htv_lvmt_的代码暂时没找到，但是可以通过添加cookie解决，建议手动添加cookie。
