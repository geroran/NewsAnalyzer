import tkinter as tk
from tkinter import messagebox, filedialog
import hashlib
import os
import requests
from bs4 import BeautifulSoup
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import Counter
import numpy as np
from PIL import Image


class NewsAnalyzer:
    def __init__(self):
        # 用户数据文件
        self.user_data_file = "user_data.txt"

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("新闻分析系统")
        self.root.geometry("800x600")

        # 设置默认字体大小
        self.default_font = ('Arial', 12)
        self.title_font = ('Arial', 16, 'bold')

        # 当前登录用户
        self.current_user = None

        # 初始化界面
        self.show_welcome_screen()

        self.root.mainloop()

    def apply_default_style(self):
        """应用默认样式"""
        self.root.option_add('*Font', self.default_font)

    # 以下是之前已有的认证系统方法
    def show_welcome_screen(self):
        """显示欢迎界面"""
        self.clear_window()
        self.apply_default_style()

        tk.Label(self.root, text="欢迎使用新闻分析系统", font=self.title_font).pack(pady=40)

        tk.Button(self.root, text="登录", command=self.show_login_screen,
                  width=20, height=2, font=self.default_font).pack(pady=15)
        tk.Button(self.root, text="注册", command=self.show_register_screen,
                  width=20, height=2, font=self.default_font).pack(pady=15)

    def show_login_screen(self):
        """显示登录界面"""
        self.clear_window()
        self.apply_default_style()

        tk.Label(self.root, text="用户登录", font=self.title_font).pack(pady=20)

        # 用户名输入
        tk.Label(self.root, text="用户名:").pack()
        self.login_username = tk.Entry(self.root, font=self.default_font)
        self.login_username.pack(pady=5)

        # 密码输入
        tk.Label(self.root, text="密码:").pack()
        self.login_password = tk.Entry(self.root, show="*", font=self.default_font)
        self.login_password.pack(pady=5)

        # 登录按钮
        tk.Button(self.root, text="登录", command=self.login_user,
                  width=15, font=self.default_font).pack(pady=20)

        # 返回按钮
        tk.Button(self.root, text="返回", command=self.show_welcome_screen,
                  width=10, font=self.default_font).pack()

    def show_register_screen(self):
        """显示注册界面"""
        self.clear_window()
        self.apply_default_style()

        tk.Label(self.root, text="用户注册", font=self.title_font).pack(pady=20)

        # 用户名输入
        tk.Label(self.root, text="用户名:").pack()
        self.register_username = tk.Entry(self.root, font=self.default_font)
        self.register_username.pack(pady=5)

        # 密码输入
        tk.Label(self.root, text="密码:").pack()
        self.register_password = tk.Entry(self.root, show="*", font=self.default_font)
        self.register_password.pack(pady=5)

        # 确认密码
        tk.Label(self.root, text="确认密码:").pack()
        self.register_confirm_password = tk.Entry(self.root, show="*", font=self.default_font)
        self.register_confirm_password.pack(pady=5)

        # 注册按钮
        tk.Button(self.root, text="注册", command=self.register_user,
                  width=15, font=self.default_font).pack(pady=20)

        # 返回按钮
        tk.Button(self.root, text="返回", command=self.show_welcome_screen,
                  width=10, font=self.default_font).pack()

    def clear_window(self):
        """清除当前窗口的所有组件"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def hash_password(self, password):
        """使用SHA-256加密密码"""
        return hashlib.sha256(password.encode()).hexdigest()

    def save_user_data(self, username, password):
        """保存用户数据到文件"""
        with open(self.user_data_file, "a") as f:
            f.write(f"{username}:{password}\n")

    def check_user_exists(self, username):
        """检查用户是否已存在"""
        if not os.path.exists(self.user_data_file):
            return False

        with open(self.user_data_file, "r") as f:
            for line in f:
                stored_username, _ = line.strip().split(":")
                if stored_username == username:
                    return True
        return False

    def verify_user(self, username, password):
        """验证用户凭据"""
        if not os.path.exists(self.user_data_file):
            return False

        hashed_password = self.hash_password(password)

        with open(self.user_data_file, "r") as f:
            for line in f:
                stored_username, stored_password = line.strip().split(":")
                if stored_username == username and stored_password == hashed_password:
                    return True
        return False

    def register_user(self):
        """注册新用户"""
        username = self.register_username.get()
        password = self.register_password.get()
        confirm_password = self.register_confirm_password.get()

        # 验证输入
        if not username or not password or not confirm_password:
            messagebox.showerror("错误", "所有字段都必须填写")
            return

        if password != confirm_password:
            messagebox.showerror("错误", "两次输入的密码不匹配")
            return

        if len(password) < 6:
            messagebox.showerror("错误", "密码长度至少为6个字符")
            return

        if self.check_user_exists(username):
            messagebox.showerror("错误", "用户名已存在")
            return

        # 加密密码并保存
        hashed_password = self.hash_password(password)
        self.save_user_data(username, hashed_password)

        messagebox.showinfo("成功", "注册成功！请登录")
        self.show_login_screen()

    def login_user(self):
        """用户登录"""
        username = self.login_username.get()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return

        if self.verify_user(username, password):
            self.current_user = username
            messagebox.showinfo("成功", f"欢迎回来，{username}！")
            self.show_main_application()
        else:
            messagebox.showerror("错误", "用户名或密码不正确")

    # 以下是新增的新闻分析功能
    def show_main_application(self):
        """显示主应用界面"""
        self.clear_window()
        self.apply_default_style()

        tk.Label(self.root, text=f"欢迎, {self.current_user}", font=self.title_font).pack(pady=20)

        # 爬取新闻按钮
        tk.Button(self.root, text="爬取百度新闻并生成词云",
                  command=self.analyze_baidu_news,
                  width=25, height=2, font=self.default_font).pack(pady=30)

        # 结果显示区域
        self.result_label = tk.Label(self.root, text="", font=self.default_font)
        self.result_label.pack(pady=20)

        # 退出按钮
        tk.Button(self.root, text="退出", command=self.show_welcome_screen,
                  width=15, font=self.default_font).pack(pady=20)

    def analyze_baidu_news(self):
        """爬取百度新闻并分析"""
        try:
            # 禁用按钮防止重复点击
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Button) and widget['text'] == "爬取百度新闻并生成词云":
                    widget.config(state=tk.DISABLED)

            self.result_label.config(text="正在爬取百度新闻...")
            self.root.update()

            # 1. 爬取百度新闻
            url = "https://news.baidu.com/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            # 2. 提取新闻文本
            self.result_label.config(text="正在提取新闻文本...")
            self.root.update()

            # 获取所有新闻标题和摘要
            news_items = []

            # 热点新闻
            hotnews = soup.find_all('div', class_='hotnews')
            for item in hotnews:
                news_items.extend(item.find_all('a'))

            # 普通新闻
            mods = soup.find_all('div', class_='mod-tab-content')
            for mod in mods:
                news_items.extend(mod.find_all('a'))

            # 提取文本并清洗
            news_texts = []
            for item in news_items:
                text = item.get_text().strip()
                if text and len(text) > 2:  # 过滤空内容和过短文本
                    news_texts.append(text)

            # 3. 保存为CSV
            self.result_label.config(text="正在保存数据...")
            self.root.update()

            df = pd.DataFrame(news_texts, columns=['新闻内容'])
            csv_path = "baidu_news.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')

            # 4. 中文分词和词频统计
            self.result_label.config(text="正在分析词频...")
            self.root.update()

            # 合并所有文本
            all_text = ' '.join(news_texts)

            # 使用jieba分词
            words = jieba.cut(all_text)
            word_list = []

            # 过滤停用词和标点符号
            stopwords = set(['的', '了', '和', '是', '在', '我', '有', '也', '都', '这', '就', '要',
                             '不', '你', '他', '她', '我们', '他们', '这个', '那个', '可以', '因为'])

            for word in words:
                if word.strip() and word not in stopwords and len(word) > 1 and not re.match('^\d+$', word):
                    word_list.append(word)

            # 统计词频
            word_counts = Counter(word_list)
            top_words = word_counts.most_common(100)

            # 5. 生成词云
            self.result_label.config(text="正在生成词云图...")
            self.root.update()

            # 生成词云
            wordcloud = WordCloud(
                font_path='simhei.ttf',  # 使用黑体
                background_color='white',
                width=800,
                height=600,
                max_words=100
            ).generate_from_frequencies(dict(top_words))

            # 保存词云图片
            img_path = "wordcloud.png"
            wordcloud.to_file(img_path)

            # 完成提示
            self.result_label.config(text=f"分析完成！\nCSV文件已保存到: {csv_path}\n词云图已保存到: {img_path}")

            # 重新启用按钮
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Button) and widget['text'] == "爬取百度新闻并生成词云":
                    widget.config(state=tk.NORMAL)

            # 显示词云图
            self.show_wordcloud(img_path)

        except Exception as e:
            self.result_label.config(text=f"发生错误: {str(e)}")
            # 重新启用按钮
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Button) and widget['text'] == "爬取百度新闻并生成词云":
                    widget.config(state=tk.NORMAL)

    def show_wordcloud(self, img_path):
        """在新窗口中显示词云图"""
        # 创建新窗口
        wordcloud_window = tk.Toplevel(self.root)
        wordcloud_window.title("词云图")
        wordcloud_window.geometry("850x650")

        # 加载图片
        img = tk.PhotoImage(file=img_path)

        # 显示图片
        label = tk.Label(wordcloud_window, image=img)
        label.image = img  # 保持引用防止被垃圾回收
        label.pack(padx=10, pady=10)

        # 关闭按钮
        tk.Button(wordcloud_window, text="关闭", command=wordcloud_window.destroy,
                  width=15, font=self.default_font).pack(pady=10)


# 运行应用
if __name__ == "__main__":
    # 检查是否安装了所需库
    try:
        import requests
        from bs4 import BeautifulSoup
        import jieba
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        import pandas as pd
    except ImportError as e:
        print(f"缺少必要的库，请先安装: {e}")
        print("可以使用以下命令安装:")
        print("pip install requests beautifulsoup4 jieba wordcloud matplotlib pandas pillow")
        exit(1)

    app = NewsAnalyzer()