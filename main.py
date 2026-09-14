import os
import re
import sys
import subprocess

try:
    import winreg
except ImportError:
    winreg = None  # 非 Windows 平台沒有 winreg，改用預設下載路徑

# ----------------------------------------------------------------------
# 🛡️ 啟動前自我修復機制：雙重檢測 PyQt6 與 yt-dlp
# ----------------------------------------------------------------------
def auto_install_requirements():
    """在 GUI 啟動前，透過 Console 檢測並自動用 pip 補齊所需套件"""
    required_packages = ["PyQt6", "yt-dlp"]
    missing_packages = []

    for pkg in required_packages:
        import_name = pkg.replace("-", "_")
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(pkg)

    if missing_packages:
        print("=" * 60)
        print(f"⚠️ 檢測到缺少以下必要 Python 套件: {', '.join(missing_packages)}")
        print("🚀 正在為您自動透過 pip 進行安裝，請稍候...")
        print("=" * 60)

        for pkg in missing_packages:
            try:
                cmd = [sys.executable, "-m", "pip", "install", "--upgrade", pkg]
                subprocess.check_call(cmd)
                print(f"✅ 【{pkg}】 安裝成功！")
            except subprocess.CalledProcessError as e:
                print(f"❌ 【{pkg}】 安裝失敗！錯誤碼：{e.returncode}")
                print("請檢查網路連線，或手動執行 'pip install PyQt6 yt-dlp'")
                sys.exit(1)
        print("\n🎉 所有必要套件部署完成，即將啟動 GUI 介面...\n")

auto_install_requirements()

# ----------------------------------------------------------------------
# 📦 套件確定存在後，才安全導入 PyQt6 模組
# ----------------------------------------------------------------------
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QDialog,
    QComboBox, QCheckBox, QGroupBox, QFileDialog, QProgressBar
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

QPushButton:disabled {
    background-color: #1e2d4a;
    color: #64748b;
    border: 1px solid #1e2d4a;
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

QPushButton#stopBtn {
    background-color: #7f1d1d;
    border: 1px solid #ef4444;
    color: #ffffff;
}

QPushButton#stopBtn:hover {
    background-color: #b91c1c;
}

QPushButton#stopBtn:disabled {
    background-color: #1e2d4a;
    color: #64748b;
    border: 1px solid #1e2d4a;
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

QProgressBar {
    background-color: #0d1a30;
    border: 1.5px solid #2a3d66;
    border-radius: 8px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #2563eb;
    border-radius: 6px;
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

QPushButton:disabled {
    background-color: #e2e8f0;
    color: #94a3b8;
    border: 1.5px solid #cbd5e1;
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

QPushButton#stopBtn {
    background-color: #dc2626;
    color: #ffffff;
    border: none;
}

QPushButton#stopBtn:hover {
    background-color: #b91c1c;
}

QPushButton#stopBtn:disabled {
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

QProgressBar {
    background-color: #eff6ff;
    border: 1.5px solid #94a3b8;
    border-radius: 8px;
    text-align: center;
    color: #0f172a;
    font-weight: bold;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #1d4ed8;
    border-radius: 6px;
}
"""

# ----------------------------------------------------------------------
# 音訊格式 / 音質選項
# ----------------------------------------------------------------------
FORMAT_OPTIONS = {
    "MP3": "mp3",
    "M4A（AAC）": "m4a",
    "Opus": "opus",
    "FLAC（無損）": "flac",
    "WAV（無損）": "wav",
    "最佳原始格式（不轉檔）": None,
}

QUALITY_OPTIONS = {
    "最高音質": "0",
    "高音質": "2",
    "中等音質": "5",
    "低音質（檔案較小）": "9",
}

PERCENT_RE = re.compile(r"\[download\]\s+(\d{1,3}(?:\.\d+)?)%")
PLAYLIST_ITEM_RE = re.compile(r"Downloading item (\d+) of (\d+)")

# ----------------------------------------------------------------------
# 工具函式
# ----------------------------------------------------------------------
def get_real_download_folder():
    if winreg is not None:
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
# 背景線程：執行音訊下載
# ----------------------------------------------------------------------
class DownloadThread(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool)  # True = 成功

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
        self.process = None
        self._stopped = False

    def run(self):
        success = False
        try:
            self.process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )

            current_item, total_items = 1, 1

            for line in self.process.stdout:
                self.log_signal.emit(line)

                item_match = PLAYLIST_ITEM_RE.search(line)
                if item_match:
                    current_item = int(item_match.group(1))
                    total_items = int(item_match.group(2))

                pct_match = PERCENT_RE.search(line)
                if pct_match:
                    pct = float(pct_match.group(1))
                    overall = ((current_item - 1) + pct / 100.0) / total_items * 100.0
                    self.progress_signal.emit(min(100, int(overall)))

            self.process.wait()

            if self._stopped:
                self.log_signal.emit("\n🛑 [STOPPED] 下載已被使用者取消\n")
                success = False
            elif self.process.returncode == 0:
                self.log_signal.emit("\n🎉 [SUCCESS] 音訊下載與轉換完成！\n")
                self.progress_signal.emit(100)
                success = True
            else:
                self.log_signal.emit(f"\n💥 [FAILED] 執行失敗，離開代碼：{self.process.returncode}\n")
                success = False
        except Exception as e:
            self.log_signal.emit(f"❌ [EXCEPTION] 發生例外錯誤：{e}\n")
            success = False
        finally:
            self.finished_signal.emit(success)

    def stop(self):
        self._stopped = True
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
            except Exception:
                pass

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
        self.resize(760, 760)
        self.setMinimumSize(720, 700)

        self.settings = QSettings("10mccxd", "YTMusicDownloader")
        self.current_theme = self.settings.value("theme", "Dark")
        self.cfg_artist = self.settings.value("cfg_artist", True, type=bool)
        self.cfg_title = self.settings.value("cfg_title", True, type=bool)
        self.cfg_thumb = self.settings.value("cfg_thumb", True, type=bool)

        saved_path = self.settings.value("output_dir", "")
        if saved_path and os.path.exists(saved_path):
            self.output_dir = saved_path
        else:
            self.output_dir = get_real_download_folder()

        self.dl_thread = None
        self.init_ui()

    def init_ui(self):
        outer_widget = QWidget()
        self.setCentralWidget(outer_widget)
        outer_layout = QVBoxLayout(outer_widget)
        outer_layout.setContentsMargins(16, 16, 16, 16)

        card = QWidget()
        card.setObjectName("mainCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(14)

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
        self.url_entry.setPlaceholderText("貼上 YouTube / YT Music 網址（單支影片或播放列表）...")
        card_layout.addWidget(self.url_entry)

        path_layout = QHBoxLayout()
        self.path_entry = QLineEdit(self.output_dir)
        browse_btn = QPushButton("瀏覽...")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.clicked.connect(self.browse_folder)

        path_layout.addWidget(self.path_entry)
        path_layout.addWidget(browse_btn)
        card_layout.addLayout(path_layout)

        # ---- 音訊格式 / 音質 ----
        format_group = QGroupBox("🎧 格式與音質")
        format_layout = QHBoxLayout()

        format_layout.addWidget(QLabel("格式:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(FORMAT_OPTIONS.keys())
        format_layout.addWidget(self.format_combo)

        format_layout.addWidget(QLabel("音質:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(QUALITY_OPTIONS.keys())
        format_layout.addWidget(self.quality_combo)

        format_group.setLayout(format_layout)
        card_layout.addWidget(format_group)

        # ---- 播放列表 ----
        playlist_group = QGroupBox("📃 播放列表")
        playlist_layout = QHBoxLayout()

        self.chk_playlist = QCheckBox("下載整個播放列表")
        self.chk_playlist.toggled.connect(self.on_playlist_toggled)
        playlist_layout.addWidget(self.chk_playlist)

        playlist_layout.addWidget(QLabel("起始:"))
        self.playlist_start = QLineEdit()
        self.playlist_start.setPlaceholderText("1")
        self.playlist_start.setFixedWidth(60)
        self.playlist_start.setEnabled(False)
        playlist_layout.addWidget(self.playlist_start)

        playlist_layout.addWidget(QLabel("結束:"))
        self.playlist_end = QLineEdit()
        self.playlist_end.setPlaceholderText("全部")
        self.playlist_end.setFixedWidth(60)
        self.playlist_end.setEnabled(False)
        playlist_layout.addWidget(self.playlist_end)

        playlist_layout.addStretch()
        playlist_group.setLayout(playlist_layout)
        card_layout.addWidget(playlist_group)

        # ---- 下載 / 停止按鈕 ----
        btn_row = QHBoxLayout()
        self.download_btn = QPushButton("🚀 開始下載")
        self.download_btn.setObjectName("primaryBtn")
        self.download_btn.setFixedHeight(42)
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.clicked.connect(self.start_download)

        self.stop_btn = QPushButton("⏹ 停止")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setFixedHeight(42)
        self.stop_btn.setFixedWidth(100)
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_download)

        btn_row.addWidget(self.download_btn)
        btn_row.addWidget(self.stop_btn)
        card_layout.addLayout(btn_row)

        # ---- 進度條 ----
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        card_layout.addWidget(self.progress_bar)

        self.open_folder_btn = QPushButton("📂 開啟下載資料夾")
        self.open_folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.open_folder_btn.setEnabled(False)
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        card_layout.addWidget(self.open_folder_btn)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        card_layout.addWidget(self.log_box)

        outer_layout.addWidget(card)

        self.append_log("✅ [SYS] 環境檢測通過 (PyQt6 & yt-dlp 已載入)\n")
        self.append_log(f"📁 [SYS] 預設下載路徑: {self.output_dir}\n")

    def on_playlist_toggled(self, checked):
        self.playlist_start.setEnabled(checked)
        self.playlist_end.setEnabled(checked)

    def append_log(self, text):
        self.log_box.moveCursor(QTextCursor.MoveOperation.End)
        self.log_box.insertPlainText(text)
        self.log_box.moveCursor(QTextCursor.MoveOperation.End)

    def browse_folder(self):
        selected = QFileDialog.getExistingDirectory(self, "選擇下載路徑", self.path_entry.text())
        if selected:
            self.path_entry.setText(selected)

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def open_output_folder(self):
        path = self.path_entry.text().strip()
        if not os.path.exists(path):
            return
        try:
            if os.name == "nt":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            self.append_log(f"❌ [ERROR] 無法開啟資料夾：{e}\n")

    def start_download(self):
        url = self.url_entry.text().strip()
        save_path = self.path_entry.text().strip()

        if not url:
            self.append_log("❌ [ERROR] 網址不能為空！\n")
            return

        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path, exist_ok=True)
                self.append_log(f"📁 [SYS] 已建立新資料夾：{save_path}\n")
            except Exception as e:
                self.append_log(f"❌ [ERROR] 儲存路徑不存在，且無法自動建立：{e}\n")
                return

        is_playlist = self.chk_playlist.isChecked()
        start_val = self.playlist_start.text().strip()
        end_val = self.playlist_end.text().strip()

        if is_playlist and start_val and not start_val.isdigit():
            self.append_log("❌ [ERROR] 播放列表「起始」需為數字！\n")
            return
        if is_playlist and end_val and not end_val.isdigit():
            self.append_log("❌ [ERROR] 播放列表「結束」需為數字！\n")
            return

        if is_playlist:
            output_template = os.path.join(save_path, "%(playlist_index)03d - %(title)s.%(ext)s")
        else:
            output_template = os.path.join(save_path, "%(title)s.%(ext)s")

        fmt_key = self.format_combo.currentText()
        fmt_value = FORMAT_OPTIONS[fmt_key]
        quality_value = QUALITY_OPTIONS[self.quality_combo.currentText()]

        cmd = [sys.executable, "-m", "yt_dlp"]

        if is_playlist:
            cmd.append("--yes-playlist")
            if start_val:
                cmd.extend(["--playlist-start", start_val])
            if end_val:
                cmd.extend(["--playlist-end", end_val])
        else:
            cmd.append("--no-playlist")

        cmd.extend(["-x", "--audio-quality", quality_value])
        if fmt_value:
            cmd.extend(["--audio-format", fmt_value])

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

        cmd.extend(["-N", "16"])
        cmd.extend([url, "-o", output_template])

        self.download_btn.setEnabled(False)
        self.download_btn.setText("下載中，請稍候...")
        self.stop_btn.setEnabled(True)
        self.open_folder_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.append_log(f"⌛ [EXEC] 開始下載任務...\nURL: {url}\nPATH: {save_path}\n" + "-" * 50 + "\n")

        self.dl_thread = DownloadThread(cmd)
        self.dl_thread.log_signal.connect(self.append_log)
        self.dl_thread.progress_signal.connect(self.progress_bar.setValue)
        self.dl_thread.finished_signal.connect(self.on_download_finished)
        self.dl_thread.start()

    def stop_download(self):
        if self.dl_thread and self.dl_thread.isRunning():
            self.dl_thread.stop()
            self.stop_btn.setEnabled(False)

    def on_download_finished(self, success):
        self.download_btn.setEnabled(True)
        self.download_btn.setText("🚀 開始下載")
        self.stop_btn.setEnabled(False)
        if success:
            self.open_folder_btn.setEnabled(True)
        else:
            self.progress_bar.setValue(0)

    def closeEvent(self, event):
        if self.dl_thread and self.dl_thread.isRunning():
            self.dl_thread.stop()
            self.dl_thread.wait(2000)

        self.settings.setValue("theme", self.current_theme)
        self.settings.setValue("cfg_artist", self.cfg_artist)
        self.settings.setValue("cfg_title", self.cfg_title)
        self.settings.setValue("cfg_thumb", self.cfg_thumb)
        self.settings.setValue("output_dir", self.path_entry.text().strip())

        event.accept()

# ----------------------------------------------------------------------
# 進入點
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    apply_theme(app, window.current_theme)
    window.show()
    sys.exit(app.exec())
