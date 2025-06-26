# 新闻分析系统 - NewsAnalyzer

## 项目简介

NewsAnalyzer 是一个基于 Python 的新闻数据分析应用，提供用户认证、新闻爬取、文本分析和可视化功能。系统通过爬取百度新闻数据，进行中文分词和词频统计，最终生成直观的词云图。

## 功能特性

- **用户认证系统**：注册/登录功能，密码SHA-256加密存储
- **新闻爬取**：自动抓取百度新闻首页内容
- **文本分析**：
  - 中文分词处理
  - 停用词过滤
  - 词频统计
- **数据可视化**：生成词云图片
- **数据导出**：保存原始新闻数据为CSV文件

## 技术栈

- 编程语言：Python 3.8+
- 核心库：
  - GUI：tkinter
  - 网络请求：requests
  - HTML解析：BeautifulSoup4
  - 中文分词：jieba
  - 词云生成：wordcloud
  - 数据处理：pandas

## 安装指南

### 环境准备

1. 确保已安装Python 3.8或更高版本
2. 推荐使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install requests beautifulsoup4 jieba wordcloud pandas pillow
```

## 使用说明

1. 启动程序：
```bash
python news_analyzer.py
```

2. 主界面流程：
   - 注册新账号或登录已有账号
   - 进入主界面后点击"爬取百度新闻并生成词云"按钮
   - 等待处理完成，查看生成的词云图

3. 输出文件：
   - `user_data.txt`：用户凭证存储文件
   - `baidu_news.csv`：爬取的新闻数据
   - `wordcloud.png`：生成的词云图片

## 项目结构

```
NewsAnalyzer/
├── news_analyzer.py    # 主程序文件
├── requirements.txt    # 依赖列表
├── user_data.txt       # 用户数据文件(运行时生成)
├── baidu_news.csv      # 新闻数据文件(运行时生成)
└── wordcloud.png       # 词云图片(运行时生成)
```

## 注意事项

1. 首次运行时需要联网获取新闻数据
2. 确保系统已安装中文字体(如黑体)以正确显示词云
3. 新闻爬取功能依赖百度新闻页面结构，如页面改版可能需要更新代码
4. 用户密码采用SHA-256加密，但仍建议不要使用重要密码

## 常见问题

Q: 词云显示乱码怎么办？
A: 请确保系统安装了中文字体，或在代码中修改font_path参数指向有效的中文字体文件

Q: 爬取新闻失败？
A: 检查网络连接，或更新User-Agent和爬取逻辑以适应网站改版

Q: 分词效果不理想？
A: 可以修改stopwords列表或添加自定义词典优化分词效果

## 开发路线图

- [ ] 增加多新闻源支持
- [ ] 添加词云自定义选项
- [ ] 改用数据库存储用户数据
- [ ] 增加历史记录功能
- [ ] 支持导出更多格式的分析结果

## 贡献指南

欢迎提交Issue或Pull Request。提交代码前请确保：
1. 代码符合PEP8规范
2. 添加适当的注释
3. 更新相关文档

## 许可证

本项目采用MIT许可证。详情见LICENSE文件。
