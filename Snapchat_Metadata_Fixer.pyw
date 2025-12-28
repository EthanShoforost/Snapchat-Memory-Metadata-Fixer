#!/usr/bin/env python3
"""
Snapchat Metadata Fixer
Created by: Ethan Shoforost
Version: 1.0.1
GitHub: https://github.com/EthanShoforost/Snapchat-Memory-Metadata-Fixer
Support: https://buymeacoffee.com/ethanshoforost

Fixes metadata for Snapchat memories by reading the date from the filename
and writing it to the file's EXIF/metadata.

Copyright (c) 2025 Ethan Shoforost
Licensed under the MIT License - see LICENSE file for details

DISCLAIMER:
This tool is not affiliated with, endorsed by, or connected to Snapchat Inc.
Use at your own risk. The creator is not responsible for any issues that may
arise from using this software. This tool modifies your files - make sure you
have backups before using.
"""

import sys
import subprocess
import os

# Package installer
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

# Check required packages
required_packages = {'piexif': 'piexif', 'Pillow': 'PIL'}
missing_packages = []
for p, i in required_packages.items():
    try:
        __import__(i)
    except ImportError:
        missing_packages.append(p)

if missing_packages:
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    
    if messagebox.askyesno("Install Libraries", 
                          f"Missing: {', '.join(missing_packages)}\n\n" +
                          "Install now? (May take 1 minute)"):
        for pkg in missing_packages:
            install_package(pkg)
        messagebox.showinfo("Success", "Libraries installed! Restarting...")
        root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        root.destroy()
        sys.exit()

import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from pathlib import Path
import shutil
import piexif
from PIL import Image

class MetadataFixer:
    def __init__(self, root):
        self.root = root
        self.root.title("Snapchat Metadata Fixer")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Colors
        self.bg = "#1a1a1a"
        self.white = "#ffffff"
        self.gray = "#2a2a2a"
        self.orange = "#FF6B35"
        self.green = "#4CAF50"
        
        self.root.configure(bg=self.bg)
        
        self.folder_path = None
        self.files_to_fix = []
        self.failed_files = []
        self.failed_details = []  # Store (file_path, error_message)
        self.fixed_count = 0
        self.failed_count = 0
        
        self.show_welcome_screen()
    
    def show_welcome_screen(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg=self.bg)
        frame.pack(expand=True)
        
        # Title
        title = tk.Label(frame, text="📅 Snapchat Metadata Fixer", 
                        font=("Arial", 28, "bold"), fg=self.white, bg=self.bg)
        title.pack(pady=20)
        
        # Description
        desc = tk.Label(frame, 
                       text="Fix the metadata on your downloaded Snapchat memories.\n\n" +
                            "This tool reads the date from your filenames and writes it\n" +
                            "to the photo/video metadata so your photo library shows\n" +
                            "the correct dates.\n\n" +
                            "Works with both photos and videos!",
                       font=("Arial", 12), fg="#cccccc", bg=self.bg, justify="center")
        desc.pack(pady=20)
        
        # Browse button
        browse_btn = self.create_canvas_button(frame, "📁  Select Memories Folder", 
                                              self.select_folder, self.orange, 250, 50)
        browse_btn.pack(pady=30)
    
    def create_canvas_button(self, parent, text, command, color, width, height):
        """Create a canvas-based button for Mac compatibility"""
        canvas = tk.Canvas(parent, width=width, height=height, 
                          bg=self.bg, highlightthickness=0)
        
        # Draw rounded rectangle
        canvas.create_rectangle(5, 5, width-5, height-5, 
                              fill=color, outline="", tags="bg")
        canvas.create_text(width/2, height/2, text=text, 
                         font=("Arial", 12, "bold"), fill=self.white, tags="text")
        
        # Hover effects
        def on_enter(e):
            canvas.config(cursor="pointinghand")
            
        def on_leave(e):
            canvas.config(cursor="")
        
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", lambda e: command())
        
        return canvas
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Snapchat Memories Folder")
        if folder:
            self.folder_path = folder
            self.scan_files()
    
    def scan_files(self):
        """Scan folder for Snapchat memory files"""
        self.files_to_fix = []
        
        # Look for files with date pattern: YYYY-MM-DD_HH-MM-SS
        for file_path in Path(self.folder_path).rglob('*'):
            if file_path.is_file():
                name = file_path.stem
                ext = file_path.suffix.lower()
                
                # Check if it's a supported file type
                if ext in ['.jpg', '.jpeg', '.png', '.mp4', '.mov']:
                    # Check if filename matches date pattern
                    if len(name) >= 19 and name[4] == '-' and name[7] == '-' and name[10] == '_':
                        self.files_to_fix.append(file_path)
        
        if not self.files_to_fix:
            messagebox.showerror("No Files Found", 
                               "No Snapchat memory files found in this folder.\n\n" +
                               "Looking for files named like:\n" +
                               "2024-03-15_14-30-45.jpg")
            return
        
        self.show_confirm_screen()
    
    def show_confirm_screen(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg=self.bg)
        frame.pack(expand=True)
        
        # Title
        title = tk.Label(frame, text="📋 Files Found", 
                        font=("Arial", 24, "bold"), fg=self.white, bg=self.bg)
        title.pack(pady=20)
        
        # Count images and videos
        images = sum(1 for f in self.files_to_fix if f.suffix.lower() in ['.jpg', '.jpeg', '.png'])
        videos = sum(1 for f in self.files_to_fix if f.suffix.lower() in ['.mp4', '.mov'])
        
        # Stats
        stats_text = f"Found {len(self.files_to_fix)} files to fix:\n\n" + \
                    f"📸 {images} photos\n" + \
                    f"🎥 {videos} videos\n\n" + \
                    f"Folder: {Path(self.folder_path).name}"
        
        stats = tk.Label(frame, text=stats_text,
                        font=("Arial", 14), fg=self.white, bg=self.bg, justify="center")
        stats.pack(pady=20)
        
        # Warning
        warning = tk.Label(frame, 
                         text="⚠️ This will modify the original files.\n" +
                              "Make sure you have a backup if needed!",
                         font=("Arial", 10), fg="#ffaa00", bg=self.bg, justify="center")
        warning.pack(pady=10)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg=self.bg)
        btn_frame.pack(pady=30)
        
        fix_btn = self.create_canvas_button(btn_frame, "✅  Fix Metadata", 
                                           self.start_fixing, self.green, 200, 50)
        fix_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = self.create_canvas_button(btn_frame, "❌  Cancel", 
                                              self.show_welcome_screen, "#666666", 200, 50)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def start_fixing(self):
        self.show_progress_screen()
        self.root.update()
        self.process_files()
    
    def show_progress_screen(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg=self.bg)
        frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        # Title
        title = tk.Label(frame, text="⚙️ Fixing Metadata", 
                        font=("Arial", 24, "bold"), fg=self.white, bg=self.bg)
        title.pack(pady=20)
        
        # Progress
        self.progress_label = tk.Label(frame, text="Starting...",
                                      font=("Arial", 12), fg=self.white, bg=self.bg)
        self.progress_label.pack(pady=10)
        
        # Progress bar background
        self.progress_bg = tk.Frame(frame, bg=self.gray, height=30)
        self.progress_bg.pack(fill=tk.X, pady=20)
        
        # Progress bar fill
        self.progress_fill = tk.Frame(self.progress_bg, bg=self.green, height=30)
        self.progress_fill.place(x=0, y=0, width=0, height=30)
        
        # Progress percentage
        self.progress_pct = tk.Label(frame, text="0%",
                                    font=("Arial", 16, "bold"), fg=self.white, bg=self.bg)
        self.progress_pct.pack(pady=10)
        
        # Stats
        self.stats_label = tk.Label(frame, text="✅ Fixed: 0  |  ❌ Failed: 0",
                                   font=("Arial", 11), fg="#cccccc", bg=self.bg)
        self.stats_label.pack(pady=10)
    
    def process_files(self):
        """Process all files and fix metadata"""
        total = len(self.files_to_fix)
        
        for i, file_path in enumerate(self.files_to_fix):
            # Update progress
            progress = (i + 1) / total
            width = int(self.progress_bg.winfo_width() * progress)
            
            self.progress_fill.place(width=width)
            self.progress_pct.config(text=f"{int(progress * 100)}%")
            self.progress_label.config(text=f"Processing: {file_path.name}")
            self.stats_label.config(text=f"✅ Fixed: {self.fixed_count}  |  ❌ Failed: {self.failed_count}")
            self.root.update()
            
            # Fix the file
            result = self.fix_file_metadata(file_path)
            if result is True:
                self.fixed_count += 1
            else:
                self.failed_count += 1
                self.failed_files.append(file_path)
                # Store the error message
                error_msg = result if isinstance(result, str) else "Unknown error"
                self.failed_details.append((file_path, error_msg))
        
        self.show_complete_screen()
    
    def fix_file_metadata(self, file_path):
        """Fix metadata for a single file - returns True on success, error string on failure"""
        try:
            # Parse date from filename
            name = file_path.stem
            
            # Check filename length
            if len(name) < 19:
                return f"Filename too short: {name}"
            
            date_str = name[:19]  # YYYY-MM-DD_HH-MM-SS
            
            # Validate date format
            try:
                dt = datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')
            except ValueError as e:
                return f"Invalid date format: {date_str} ({str(e)})"
            
            ext = file_path.suffix.lower()
            
            # Check file type
            if ext not in ['.jpg', '.jpeg', '.png', '.mp4', '.mov']:
                return f"Unsupported file type: {ext}"
            
            if ext in ['.jpg', '.jpeg']:
                return self.fix_jpeg_metadata(file_path, dt)
            elif ext == '.png':
                return self.fix_png_metadata(file_path, dt)
            elif ext in ['.mp4', '.mov']:
                return self.fix_video_metadata(file_path, dt)
            
            return "Unknown error"
            
        except Exception as e:
            return f"Exception: {str(e)}"
    
    def fix_jpeg_metadata(self, file_path, dt):
        """Fix EXIF metadata for JPEG files - returns True or error string"""
        try:
            # Format datetime for EXIF (YYYY:MM:DD HH:MM:SS)
            exif_dt = dt.strftime('%Y:%m:%d %H:%M:%S')
            
            # Try to load existing EXIF
            try:
                exif_dict = piexif.load(str(file_path))
            except Exception as e:
                exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
            
            # Set date/time fields
            exif_dict["0th"][piexif.ImageIFD.DateTime] = exif_dt.encode()
            exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = exif_dt.encode()
            exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = exif_dt.encode()
            
            # Convert to bytes
            exif_bytes = piexif.dump(exif_dict)
            
            # Save with EXIF
            img = Image.open(file_path)
            img.save(file_path, exif=exif_bytes, quality=95)
            
            # Update file modification time
            timestamp = dt.timestamp()
            os.utime(file_path, (timestamp, timestamp))
            
            return True
            
        except Exception as e:
            return f"JPEG error: {str(e)}"
    
    def fix_png_metadata(self, file_path, dt):
        """Fix metadata for PNG files (no EXIF, just file times) - returns True or error string"""
        try:
            # PNG doesn't have EXIF, just update file modification time
            timestamp = dt.timestamp()
            os.utime(file_path, (timestamp, timestamp))
            return True
        except Exception as e:
            return f"PNG error: {str(e)}"
    
    def fix_video_metadata(self, file_path, dt):
        """Fix metadata for video files using ffmpeg - returns True or error string"""
        try:
            # Format for ffmpeg metadata
            creation_time = dt.strftime('%Y-%m-%dT%H:%M:%S')
            
            # Create temp file
            temp_file = file_path.with_suffix(file_path.suffix + '.tmp')
            
            # Use ffmpeg to copy video with new metadata
            cmd = [
                'ffmpeg', '-i', str(file_path),
                '-c', 'copy',  # Copy without re-encoding
                '-metadata', f'creation_time={creation_time}',
                '-y',  # Overwrite
                str(temp_file)
            ]
            
            # Try to run ffmpeg
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode == 0 and temp_file.exists():
                # Replace original with temp
                shutil.move(str(temp_file), str(file_path))
                
                # Update file times
                timestamp = dt.timestamp()
                os.utime(file_path, (timestamp, timestamp))
                
                return True
            else:
                # FFmpeg failed or not installed - just update file times
                if temp_file.exists():
                    temp_file.unlink()
                
                timestamp = dt.timestamp()
                os.utime(file_path, (timestamp, timestamp))
                return True
                
        except Exception as e:
            # Fallback: just update file times
            try:
                timestamp = dt.timestamp()
                os.utime(file_path, (timestamp, timestamp))
                return True
            except Exception as e2:
                return f"Video error: {str(e2)}"
    
    def show_complete_screen(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg=self.bg)
        frame.pack(expand=True)
        
        # Title
        if self.failed_count == 0:
            title = tk.Label(frame, text="✅ Complete!", 
                            font=("Arial", 28, "bold"), fg=self.green, bg=self.bg)
        else:
            title = tk.Label(frame, text="⚠️ Complete with Errors", 
                            font=("Arial", 28, "bold"), fg=self.orange, bg=self.bg)
        title.pack(pady=30)
        
        # Results
        results_text = f"Successfully fixed: {self.fixed_count} files\n"
        if self.failed_count > 0:
            results_text += f"Failed: {self.failed_count} files\n\n"
            results_text += "You can retry the failed files below."
        else:
            results_text += "\nYour photos and videos now have the correct dates!"
        
        results = tk.Label(frame, text=results_text,
                          font=("Arial", 14), fg=self.white, bg=self.bg, justify="center")
        results.pack(pady=20)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg=self.bg)
        btn_frame.pack(pady=30)
        
        # View Errors button (only if there are failures)
        if self.failed_count > 0:
            view_errors_btn = self.create_canvas_button(btn_frame, "📋  View Errors", 
                                                       self.show_error_details, "#666666", 180, 50)
            view_errors_btn.pack(side=tk.LEFT, padx=10)
        
        # Retry button (only if there are failures)
        if self.failed_count > 0:
            retry_btn = self.create_canvas_button(btn_frame, f"🔄  Retry Failed ({self.failed_count})", 
                                                  self.retry_failed, self.orange, 200, 50)
            retry_btn.pack(side=tk.LEFT, padx=10)
        
        # Done button
        done_btn = self.create_canvas_button(btn_frame, "✨  Done", 
                                            self.root.quit, self.green, 200, 50)
        done_btn.pack(side=tk.LEFT, padx=10)
    
    def show_error_details(self):
        """Show detailed error information in a new window"""
        error_window = tk.Toplevel(self.root)
        error_window.title("Error Details")
        error_window.geometry("800x500")
        error_window.configure(bg=self.bg)
        
        # Title
        title = tk.Label(error_window, text="Failed Files - Error Details",
                        font=("Arial", 16, "bold"), fg=self.white, bg=self.bg)
        title.pack(pady=20)
        
        # Scrollable frame
        frame = tk.Frame(error_window, bg=self.bg)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget for errors
        text = tk.Text(frame, bg=self.gray, fg=self.white, 
                      font=("Courier", 10), yscrollcommand=scrollbar.set,
                      wrap=tk.WORD, padx=10, pady=10)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        
        # Add error details
        for i, (file_path, error) in enumerate(self.failed_details, 1):
            text.insert(tk.END, f"{i}. ", "number")
            text.insert(tk.END, f"{file_path.name}\n", "filename")
            text.insert(tk.END, f"   Error: {error}\n\n", "error")
        
        # Configure tags for colors
        text.tag_config("number", foreground="#FFD700")
        text.tag_config("filename", foreground="#FF6B35", font=("Courier", 10, "bold"))
        text.tag_config("error", foreground="#cccccc")
        
        text.config(state=tk.DISABLED)  # Make read-only
        
        # Close button
        close_btn = self.create_canvas_button(error_window, "Close", 
                                             error_window.destroy, self.orange, 150, 40)
        close_btn.pack(pady=20)
    
    def retry_failed(self):
        """Retry fixing failed files"""
        if not self.failed_files:
            return
        
        # Reset counters for retry
        self.files_to_fix = self.failed_files.copy()
        self.failed_files = []
        self.failed_details = []  # Clear old error details
        retry_fixed = self.fixed_count
        retry_failed = self.failed_count
        self.fixed_count = 0
        self.failed_count = 0
        
        # Show progress screen and process
        self.show_progress_screen()
        self.root.update()
        self.process_files()

if __name__ == "__main__":
    root = tk.Tk()
    app = MetadataFixer(root)
    root.mainloop()
