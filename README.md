#Python学习笔记1（爬虫）

---

###相关知识点

* **bs4** 库中 **BeautifulSoup** 的使用
* python**多线程**的使用
* python读写本地文件

##实现步骤
### 1. 确定目标

公司的王总之前想让我帮忙抓取一个电影资源网站的页面数据，我因琐事缠身一直没答应，这几天正好公司没事，抽空学习了python语法，正好借此机会练练手。

目标确定：**抓取电影资源网站的资源数据**

### 2. 查阅资料
在网上花了点时间查了查python爬虫的实现方式，有几种：

&ensp;&ensp;(1) 通过正则匹配
&ensp;&ensp;(2) 通过BeautifulSoup
&ensp;&ensp;(3) 通过Lxml匹配

因为偷懒 选择了较为简单的BeautifulSoup的实现方式
### 3. 编码实现

&ensp;&ensp;首先导入`requests`库`bs4`库下的`BeautifulSoup`模块

```
import requests
from bs4 import BeautifulSoup
```

接着查看需要爬取页面的元素 网址如下

`https://www.okzy.co/?m=vod-detail-id-1.html`

经过观察发现该网站的影视详情页面都是以`id-数字`区分 由此规律可以做出判断 影视详情页公用一套模板 影视资源以id递增

```

 vod_list = [] # 存储每个页面获取的json
	 for i in range(start_count, end_count + 1):

	    url = 'https://www.okzy.co/?m=vod-detail-id-' + str(i) + '.html'

	    wb_data = requests.get(url)  # 获取页面html

	    if wb_data == None :
	        continue

	    wb_data.encoding = 'utf-8'
	    soup = BeautifulSoup(wb_data.text, 'html.parser') # 对页面进行解析
```

其中 start_count 为起始页的id end_count+1 为结束页的id

soup 则是已解析过的html页面
通过分析页面元素 发现需要获取数据的几个地方分别在不同的div标签下 由此 抽出几个函数 根据返回的soup页面信息 分别获取标签下的数据

```
# 获取视频封面
def get_vod_img(soup):

# 获取视频信息
def get_vod_info(soup):

# 获取剧情介绍
def get_vod_des(soup):

# 获取播放链接
def get_vod_play_link(soup):
```

几个函数的内容都很简单 通过soup的`select`函数 获取对应的标签内容或链接 因为最终是想要将这些数据封装成json 所以都转成了字符串 例如：获取剧情介绍

```
 des_label = soup.select('.vodplayinfo')
    vod_des = des_label[1].get_text()
    return vod_des
```

其中`select`函数返回的是符合查找条件的标签数组 这里是根据div的class名直接获取数组第一个的数据

关于**BeautifulSoup**的`select`函数及其他函数的用法 可以自行百度 这里不多做介绍 只用记住这是一个根据参数筛选获取对应标签的函数即可

将获取的数据封装成json：

```
	vod_json = {}

	vod_json['img'] = vod_img

	vod_json['info'] = vod_info

	vod_json['des'] = vod_des

	vod_json['link'] = vod_play_link

	vod_list.append(vod_json)
```

这样 **vod_list** 就是我们最终获取所有页面信息的数组
将这个数组也封装成json 写入本地文件

```
 json = {}
    json['data'] = vod_list
    print(json)
    json_file_util.write('data_' + file_name, json)
```

经过试验 发现如果单线程抓取数据 效率很慢 所以 考虑用多线程同时抓取 将循环抓取页面的函数抽出

```
# 循环爬取页面 并将数据写入json
def loop_request(start_count, end_count, file_name):
```

这样 只需传入起始页码 跟文件名即可

将开启多线程的操作放到`__main__`函数下 代码如下

```

    # 起始页码
    page_start = 1

    # 结束页码
    page_end = 35

    # 每集合页数
    page_count = 10

    # 每集合(page_count条数据)开启一条线程

    # 创建线程
    threads = []
    times = int((page_end - page_start)/page_count) + 1
    print('times == ' + str(times))
    for i in range(times):
        s = page_start + page_count * i
        if page_end <= page_count:
            e = page_end
        else:
            if i == times-1:
                e = page_end % page_count + page_count * i
            else:
                e = page_count * (i + 1)
                print('s == ' + str(s) + ' e == ' + str(e))

        t = threading.Thread(target=loop_request,args=(s,e,str(s) + '_' + str(e)))
        threads.append(t)

    for i in range(times):
        threads[i].start()
    for i in range(times):
        threads[i].join()
```

大意为根据定义三个变量 **起始页数**  **结束页数**  **每个线程抓取的数量**

经过实验 效率还算可以 2000个页面分4个线程不到3分钟就抓取完毕


##结束
至此 这次爬虫练手算是结束

总结一下：python动态的语法让代码简洁了很多 执行效率也不错 爬虫的框架多种多样 选择合适的即可 目的都是为了获取想要的数据