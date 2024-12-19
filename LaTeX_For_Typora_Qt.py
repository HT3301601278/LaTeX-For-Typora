from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QTextEdit, QFrame)
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
import sys
import re
import pyperclip

class LatexConverterQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LaTeX For Typora 公式转换器")
        self.setMinimumSize(900, 700)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #2c3e50;
            }
            QTextEdit {
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 10px;
                background-color: white;
                selection-background-color: #bdc3c7;
                min-height: 150px;
            }
            QTextEdit:focus {
                border: 2px solid #2980b9;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2574a9;
            }
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建主布局
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 设置字体
        title_font = QFont("Microsoft YaHei UI", 12, QFont.Weight.DemiBold)
        
        # 创建输入区域
        input_frame = QFrame()
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 15, 15, 15)
        
        input_label = QLabel("输入 LaTeX 公式:")
        input_label.setFont(title_font)
        self.input_text = QTextEdit()
        self.input_text.setMinimumHeight(200)
        
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addStretch(1)
        
        self.convert_btn = QPushButton("转换")
        self.remove_empty_btn = QPushButton("去除空行")
        self.copy_btn = QPushButton("复制结果")
        self.clear_btn = QPushButton("清空")
        
        # 设置按钮样式
        for btn in [self.convert_btn, self.remove_empty_btn, self.copy_btn, self.clear_btn]:
            btn.setFixedSize(150, 45)
        
        self.remove_empty_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        # 按新顺序添加按钮到布局
        button_layout.addWidget(self.convert_btn)
        button_layout.addWidget(self.remove_empty_btn)
        button_layout.addWidget(self.copy_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch(1)
        
        # 创建输出区域
        output_frame = QFrame()
        output_layout = QVBoxLayout(output_frame)
        output_layout.setContentsMargins(15, 15, 15, 15)
        
        output_label = QLabel("转换结果:")
        output_label.setFont(title_font)
        self.output_text = QTextEdit()
        self.output_text.setMinimumHeight(200)
        self.output_text.setReadOnly(True)
        
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        
        # 状态标签
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #7f8c8d;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # 添加所有部件到主布局
        layout.addWidget(input_frame)
        layout.addLayout(button_layout)
        layout.addWidget(output_frame)
        layout.addWidget(self.status_label)
        
        # 连接信号和槽
        self.convert_btn.clicked.connect(self.convert)
        self.copy_btn.clicked.connect(self.copy_result)
        self.clear_btn.clicked.connect(self.clear_all)
        self.remove_empty_btn.clicked.connect(self.remove_empty_lines)
        
    def convert_latex_format(self, text):
        # 处理 \[...\] 格式
        text = re.sub(r'\\\[(.*?)\\\]', r'$\1$', text, flags=re.DOTALL)
        # 处理 \(...\) 格式
        text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text, flags=re.DOTALL)
        return text
    
    def convert(self):
        input_text = self.input_text.toPlainText()
        converted_text = self.convert_latex_format(input_text)
        self.output_text.setPlainText(converted_text)
        self.status_label.setText("转换完成")
    
    def copy_result(self):
        output_text = self.output_text.toPlainText()
        pyperclip.copy(output_text)
        self.status_label.setText("已复制到剪贴板")
        
    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()
        self.status_label.setText("已清空")
    
    def remove_empty_lines(self):
        """去除空行"""
        text = self.output_text.toPlainText()
        if not text:
            text = self.input_text.toPlainText()
            
        # 去除空行，保留包含实际内容的行
        lines = [line for line in text.splitlines() if line.strip()]
        result = '\n'.join(lines)
        
        self.output_text.setPlainText(result)
        self.status_label.setText("已去除空行")

def main():
    app = QApplication(sys.argv)
    window = LatexConverterQt()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 