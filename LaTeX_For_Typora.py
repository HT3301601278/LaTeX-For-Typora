import re
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import pyperclip
import ctypes

class LatexConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LaTeX For Typora 公式转换器")
        
        # 获取屏幕DPI缩放比例
        try:
            # Windows系统
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        except:
            # 其他系统
            scaleFactor = root.winfo_fpixels('1i') / 72
            
        # 基于DPI缩放调整基础字体大小
        self.font_size = int(10 * scaleFactor)
        default_font = ('Microsoft YaHei UI', self.font_size)  # 使用微软雅黑作为默认字体
        
        # 设置默认字体
        self.root.option_add('*Font', default_font)
        
        # 调整窗口默认大小
        window_width = int(800 * scaleFactor)
        window_height = int(600 * scaleFactor)
        self.root.geometry(f"{window_width}x{window_height}")
        
        # 创建主框架并设置权重
        main_frame = ttk.Frame(root)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)  # 输入框行
        main_frame.grid_rowconfigure(4, weight=1)  # 输出框行
        
        # 输入区域标签
        ttk.Label(main_frame, text="输入LaTeX公式:", 
                 font=('Microsoft YaHei UI', int(11 * scaleFactor))).grid(
                     row=0, column=0, sticky=tk.W, padx=10)
        
        # 输入文本框 - 增加weight使其能够扩展
        self.input_text = scrolledtext.ScrolledText(
            main_frame, 
            height=10,
            wrap=tk.WORD,
            font=('Consolas', self.font_size)
        )
        self.input_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        # 按钮区域的调整
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        # 调整按钮样式
        style = ttk.Style()
        style.configure('Custom.TButton', 
                      font=('Microsoft YaHei UI', int(10 * scaleFactor)),
                      padding=(int(20 * scaleFactor), int(10 * scaleFactor)))  # 增加按钮内边距
        
        # 按钮样式参数
        button_style = {
            'style': 'Custom.TButton',
            'width': 15  # 增加按钮宽度
        }
        
        # 创建更大的按钮
        ttk.Button(button_frame, 
                  text="转换", 
                  command=self.convert, 
                  **button_style).pack(side=tk.LEFT, padx=int(10 * scaleFactor))
        
        ttk.Button(button_frame, 
                  text="复制结果", 
                  command=self.copy_result,
                  **button_style).pack(side=tk.LEFT, padx=int(10 * scaleFactor))
        
        ttk.Button(button_frame, 
                  text="清空", 
                  command=self.clear_all,
                  **button_style).pack(side=tk.LEFT, padx=int(10 * scaleFactor))
        
        # 输出区域标签
        ttk.Label(main_frame, text="转换结果:", 
                 font=('Microsoft YaHei UI', int(11 * scaleFactor))).grid(
                     row=3, column=0, sticky=tk.W, padx=10)
        
        # 输出文本框 - 增加weight使其能够扩展
        self.output_text = scrolledtext.ScrolledText(
            main_frame,
            height=10,
            wrap=tk.WORD,
            font=('Consolas', self.font_size)
        )
        self.output_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text="", 
                                    font=('Microsoft YaHei UI', int(9 * scaleFactor)))
        self.status_label.grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        
        # 配置主窗口的网格权重
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        
    def convert_latex_format(self, text):
        # 处理 \[...\] 格式
        text = re.sub(r'\\\[(.*?)\\\]', r'$\1$', text, flags=re.DOTALL)
        # 处理 \(...\) 格式
        text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text, flags=re.DOTALL)
        return text
    
    def convert(self):
        input_text = self.input_text.get("1.0", tk.END)
        converted_text = self.convert_latex_format(input_text)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", converted_text)
        self.status_label.config(text="转换完成")
    
    def copy_result(self):
        output_text = self.output_text.get("1.0", "end-1c")
        pyperclip.copy(output_text)
        self.status_label.config(text="已复制到剪贴板")
        
    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.status_label.config(text="已清空")

def main():
    root = tk.Tk()
    app = LatexConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()