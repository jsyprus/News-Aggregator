import requests
import json
import tkinter as tk
import webbrowser


class NewsAggregator(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.topic_label = tk.Label(
            self, text="Enter topic:", font=("Arial Bold", 16))
        self.topic_label.pack(pady=10)

        self.topic_input = tk.Entry(self, font=("Arial", 14))
        self.topic_input.pack()

        self.search_button = tk.Button(self, text="Search", font=(
            "Arial Bold", 14), command=self.search)
        self.search_button.pack(pady=10)

        self.text = tk.Text(self, font=("Arial", 12), width=80, state='disabled')
        self.text.pack(padx=20, pady=20)

    def search(self):
        topic = self.topic_input.get()
        if not topic:
            return

        self.text.config(state='normal')
        self.text.delete('1.0', tk.END)
        api_key = "b1118beda5bb4f86b1c1096cfbe4ba6f"
        url = f"https://newsapi.org/v2/top-headlines?q={topic}&apiKey={api_key}"
        response = requests.get(url)
        data = response.json()
        articles = data["articles"]

        self.text.tag_configure('bold', font=('Arial', 12, 'bold'))
        self.text.tag_configure('italic', font=('Arial', 10, 'italic'), foreground='gray')
        self.text.tag_configure('clickable', foreground='blue', underline=True)

        for article in articles:
            title = article['title']
            description = article['description']
            url = article['url']
            self.text.insert(tk.END, title + '\n', ('bold', 'clickable'))
            self.text.insert(tk.END, f"\t\u2022 {description}\n\n", ('italic',))
            self.text.tag_add('clickable', f'{self.text.index("end-2l")} linestart', f'{self.text.index("end-2l")} lineend')
            self.text.tag_bind('clickable', '<Button-1>', lambda e, url=url: self.open_url(url))

        self.text.config(state='disabled')

    def open_url(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    root = tk.Tk()
    app = NewsAggregator(master=root)
    app.mainloop()
