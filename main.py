import os
import sys
import winreg
import subprocess
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QDialog,
    QComboBox, QCheckBox, QGroupBox
)

# ----------------------------------------------------------------------
# 🎨 10m.cc.cd 風格 - 高對比度樣式表
# ----------------------------------------------------------------------
STYLE_DARK = """
QMainWindow, QDialog {
    background-color: #0b1329;
}

QWidget {
    color: #FFFFFF;
    font-family: 'Noto Sans', 'Segoe UI', 'Microsoft JhengHei', sans-serif;
    font-size: 13px;
}

#mainCard {
    background-color: #162032;
    border: 1px solid #2a3d66;
    border-radius: 16px;
}

#mainTitle {
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
}

QGroupBox {
    background-color: #162032;
    border: 1px solid #2a3d66;
    border-radius: 12px;
    margin-top: 12px;
    padding-top: 14px;
    font-weight: bold;
    color: #60a5fa;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 4px;
}

QLineEdit {
    background-color: #0d1a30;
    border: 1.5px solid #2563eb;
    border-radius: 8px;
    padding: 10px 12px;
    color: #60a5fa;
    font-weight: bold;
    selection-background-color: #3b82f6;
    selection-color: #ffffff;
}

QLineEdit:focus {
    border: 2px solid #60a5fa;
    background-color: #13233d;
}

QPushButton {
    background-color: #1a2a47;
    border: 1px solid #3b82f6;
    border-radius: 8px;
    padding: 8px 14px;
    color: #ffffff;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #2563eb;
    color: #ffffff;
    border-color: #60a5fa;
}

QPushButton:pressed {
    background-color: #1d4ed8;
}

QPushButton#primaryBtn {
    background-color: #2563eb;
    color: #ffffff;
    border: 1px solid #60a5fa;
    font-weight: bold;
    font-size: 15px;
}

QPushButton#primaryBtn:hover {
    background-color: #3b82f6;
}

QPushButton#primaryBtn:disabled {
    background-color: #1e2d4a;
    color: #64748b;
    border: none;
}

QTextEdit {
    background-color: #050a14;
    border: 1.5px solid #1e2d4a;
    border-radius: 10px;
    color: #38bdf8;
    font-family: 'Consolas', 'Cascadia Code', monospace;
    font-size: 13px;
    font-weight: 500;
    padding: 10px;
}

QComboBox {
    background-color: #1a2a47;
    border: 1px solid #3b82f6;
    border-radius: 8px;
    padding: 6px 10px;
    color: #ffffff;
    font-weight: 600;
}

QComboBox QAbstractItemView {
    background-color: #162032;
    border: 1px solid #3b82f6;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    color: #ffffff;
    padding: 4px;
}

QCheckBox {
    color: #ffffff;
    font-weight: 500;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1.5px solid #3b82f6;
    background-color: #0b1329;
}

QCheckBox::indicator:hover {
    border-color: #60a5fa;
}

QCheckBox::indicator:checked {
    background-color: #2563eb;
    border-color: #60a5fa;
}
"""

STYLE_LIGHT = """
QMainWindow, QDialog {
    background-color: #f1f5f9;
}

QWidget {
    color: #0f172a;
    font-family: 'Noto Sans', 'Segoe UI', 'Microsoft JhengHei', sans-serif;
    font-size: 13px;
}

#mainCard {
    background-color: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 16px;
}

#mainTitle {
    font-size: 18px;
    font-weight: bold;
    color: #0f172a;
}

QGroupBox {
    background-color: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 12px;
    margin-top: 12px;
    padding-top: 14px;
    font-weight: bold;
    color: #1d4ed8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 4px;
}

QLineEdit {
    background-color: #eff6ff;
    border: 1.5px solid #3b82f6;
    border-radius: 8px;
    padding: 10px 12px;
    color: #1e40af;
    font-weight: bold;
}

QLineEdit:focus {
    border: 2px solid #1d4ed8;
    background-color: #ffffff;
}

QPushButton {
    background-color: #f8fafc;
    border: 1.5px solid #94a3b8;
    border-radius: 8px;
    padding: 8px 14px;
    color: #0f172a;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #e2e8f0;
    border-color: #64748b;
}

QPushButton#primaryBtn {
    background-color: #1d4ed8;
    color: #ffffff;
    border: none;
    font-weight: bold;
    font-size: 15px;
}

QPushButton#primaryBtn:hover {
    background-color: #1e40af;
}

QPushButton#primaryBtn:disabled {
    background-color: #cbd5e1;
    color: #64748b;
}

QTextEdit {
    background-color: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 10px;
    color: #0f172a;
    font-family: 'Consolas', monospace;
    font-size: 13px;
    font-weight: 600;
    padding: 10px;
}

QComboBox {
    background-color: #ffffff;
    border: 1.5px solid #94a3b8;
    border-radius: 8px;
    padding: 6px 10px;
    color: #0f172a;
    font-weight: bold;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #94a3b8;
    selection-background-color: #1d4ed8;
    selection-color: #ffffff;
    color: #0f172a;
    padding: 4px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1.5px solid #64748b;
    background-color: #ffffff;
}

QCheckBox::indicator:checked {
    background-color: #1d4ed8;
    border-color: #1d4ed8;
}
"""

# ----------------------------------------------------------------------
# 工具函式
# ----------------------------------------------------------------------
def get_real_download_folder():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        )
        path, _ = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")
        winreg.CloseKey(key)
        real_path = os.path.expandvars(path)
        if os.path.exists(real_path):
            return real_path
    except Exception:
        pass
    return os.path.join(os.path.expanduser("~"), "Downloads")

def apply_theme(app, mode_name):
    if mode_name == "Dark":
        app.setStyleSheet(STYLE_DARK)
    else:
        app.setStyleSheet(STYLE_LIGHT)

# ----------------------------------------------------------------------
# 背景線程：自動 pip install
# ----------------------------------------------------------------------
class PipInstallThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)

    def run(self):
        self.log_signal.emit("⚠️ 檢測到尚未安裝 yt-dlp 套件，正在自動透過 pip 安裝...\n")
        try:
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )
            for line in process.stdout:
                self.log_signal.emit(line)
            process.wait()

            if process.returncode == 0:
                self.log_signal.emit("✅ yt-dlp 套件安裝成功！\n\n")
                self.finished_signal.emit(True)
            else:
                self.log_signal.emit(f"❌ pip 安裝失敗，錯誤代碼：{process.returncode}\n\n")
                self.finished_signal.emit(False)
        except Exception as e:
            self.log_signal.emit(f"❌ 自動安裝失敗：{e}\n\n")
            self.finished_signal.emit(False)

# ----------------------------------------------------------------------
# 背景線程：執行音訊下載
# ----------------------------------------------------------------------
class DownloadThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        try:
            process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )

            for line in process.stdout:
                self.log_signal.emit(line)

            process.wait()
            if process.returncode == 0:
                self.log_signal.emit("\n🎉 [SUCCESS] 音訊下載與轉換完成！\n")
            else:
                self.log_signal.emit(f"\n💥 [FAILED] 執行失敗，離開代碼：{process.returncode}\n")
        except Exception as e:
            self.log_signal.emit(f"❌ [EXCEPTION] 發生例外錯誤：{e}\n")
        finally:
            self.finished_signal.emit()

# ----------------------------------------------------------------------
# ⚙️ 設定彈窗
# ----------------------------------------------------------------------
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setWindowTitle("⚙️ 下載與偏好設定")
        self.setFixedSize(380, 340)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        theme_group = QGroupBox("🎨 外觀與主題")
        theme_layout = QVBoxLayout()
        mode_layout = QHBoxLayout()
        mode_label = QLabel("模式切換:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Dark", "Light"])
        self.mode_combo.setCurrentText(self.main_window.current_theme)
        self.mode_combo.currentTextChanged.connect(self.on_mode_change)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        theme_layout.addLayout(mode_layout)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        meta_group = QGroupBox("🎵 元資料 (Metadata) 寫入")
        meta_layout = QVBoxLayout()
        self.chk_artist = QCheckBox("寫入歌手資訊")
        self.chk_artist.setChecked(self.main_window.cfg_artist)
        self.chk_artist.toggled.connect(lambda v: setattr(self.main_window, 'cfg_artist', v))

        self.chk_title = QCheckBox("寫入歌名標題")
        self.chk_title.setChecked(self.main_window.cfg_title)
        self.chk_title.toggled.connect(lambda v: setattr(self.main_window, 'cfg_title', v))

        self.chk_thumb = QCheckBox("嵌入專輯封面")
        self.chk_thumb.setChecked(self.main_window.cfg_thumb)
        self.chk_thumb.toggled.connect(lambda v: setattr(self.main_window, 'cfg_thumb', v))

        meta_layout.addWidget(self.chk_artist)
        meta_layout.addWidget(self.chk_title)
        meta_layout.addWidget(self.chk_thumb)
        meta_group.setLayout(meta_layout)
        layout.addWidget(meta_group)

        close_btn = QPushButton("確定並關閉")
        close_btn.setObjectName("primaryBtn")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def on_mode_change(self, mode):
        self.main_window.current_theme = mode
        apply_theme(QApplication.instance(), mode)

# ----------------------------------------------------------------------
# 主視窗
# ----------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("10m.cc.cd 風格 - YT 音訊下載器")
        self.setFixedSize(720, 580)

        self.current_theme = "Dark"
        self.cfg_artist = True
        self.cfg_title = True
        self.cfg_thumb = True

        self.output_dir = get_real_download_folder()

        self.init_ui()
        self.check_ytdlp_installed()

    def init_ui(self):
        outer_widget = QWidget()
        self.setCentralWidget(outer_widget)
        outer_layout = QVBoxLayout(outer_widget)
        outer_layout.setContentsMargins(16, 16, 16, 16)

        card = QWidget()
        card.setObjectName("mainCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        top_layout = QHBoxLayout()
        title_label = QLabel("✉️ YT Music 音訊下載器")
        title_label.setObjectName("mainTitle")

        settings_btn = QPushButton("⚙️ 設定")
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.clicked.connect(self.open_settings)

        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(settings_btn)
        card_layout.addLayout(top_layout)

        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("貼上 YouTube / YT Music 網址...")
        card_layout.addWidget(self.url_entry)

        path_layout = QHBoxLayout()
        self.path_entry = QLineEdit(self.output_dir)
        browse_btn = QPushButton("瀏覽...")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.clicked.connect(self.browse_folder)

        path_layout.addWidget(self.path_entry)
        path_layout.addWidget(browse_btn)
        card_layout.addLayout(path_layout)

        self.download_btn = QPushButton("🚀 開始下載 MP3")
        self.download_btn.setObjectName("primaryBtn")
        self.download_btn.setFixedHeight(42)
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.clicked.connect(self.start_download)
        card_layout.addWidget(self.download_btn)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        card_layout.addWidget(self.log_box)

        outer_layout.addWidget(card)

        self.append_log(f"📁 [SYS] 預設下載路徑: {self.output_dir}\n")

    def check_ytdlp_installed(self):
        """檢查環境中是否有 yt-dlp"""
        try:
            import yt_dlp
            self.append_log("✅ [SYS] 已成功載入 pip yt-dlp 環境！\n")
        except ImportError:
            self.download_btn.setEnabled(False)
            self.download_btn.setText("正在安裝 yt-dlp 套件...")
            self.pip_thread = PipInstallThread()
            self.pip_thread.log_signal.connect(self.append_log)
            self.pip_thread.finished_signal.connect(self.on_pip_finished)
            self.pip_thread.start()

    def on_pip_finished(self, success):
        self.download_btn.setEnabled(True)
        self.download_btn.setText("🚀 開始下載 MP3")

    def append_log(self, text):
        self.log_box.moveCursor(self.log_box.textCursor().MoveOperation.End)
        self.log_box.insertPlainText(text)
        self.log_box.moveCursor(self.log_box.textCursor().MoveOperation.End)

    def browse_folder(self):
        selected = QFileDialog.getExistingDirectory(self, "選擇下載路徑", self.path_entry.text())
        if selected:
            self.path_entry.setText(selected)

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def start_download(self):
        url = self.url_entry.text().strip()
        save_path = self.path_entry.text().strip()

        if not url:
            self.append_log("❌ [ERROR] 網址不能為空！\n")
            return
        if not os.path.exists(save_path):
            self.append_log("❌ [ERROR] 儲存路徑不存在！\n")
            return

        output_template = os.path.join(save_path, "%(title)s.%(ext)s")

        # 使用目前 Python 環境下的 yt-dlp module 指令
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--no-playlist",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--concurrent-fragments", "16",
            "-N", "16"
        ]

        need_add_metadata = False
        if self.cfg_artist:
            cmd.extend(["--parse-metadata", "%(artist,uploader)s:%(meta_artist)s"])
            need_add_metadata = True
        if self.cfg_title:
            cmd.extend(["--parse-metadata", "%(title)s:%(meta_title)s"])
            need_add_metadata = True
        if need_add_metadata:
            cmd.append("--add-metadata")
        if self.cfg_thumb:
            cmd.append("--embed-thumbnail")

        cmd.extend([url, "-o", output_template])

        self.download_btn.setEnabled(False)
        self.download_btn.setText("下載中，請稍候...")
        self.append_log(f"⌛ [EXEC] 開始下載任務...\nURL: {url}\nPATH: {save_path}\n" + "-"*50 + "\n")

        self.dl_thread = DownloadThread(cmd)
        self.dl_thread.log_signal.connect(self.append_log)
        self.dl_thread.finished_signal.connect(self.on_download_finished)
        self.dl_thread.start()

    def on_download_finished(self):
        self.download_btn.setEnabled(True)
        self.download_btn.setText("🚀 開始下載 MP3")

# ----------------------------------------------------------------------
# 進入點
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_theme(app, "Dark")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
