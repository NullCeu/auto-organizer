#!/usr/bin/env python3
"""
Organizador Automático de Arquivos
Organiza arquivos automaticamente por tipo, data ou regras personalizadas
"""

import os
import json
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
from pathlib import Path
from threading import Thread
import time

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

class FileOrganizer:
    def __init__(self):
        self.config_file = "organizer_config.json"
        self.default_config = {
            "rules": {
                "images": {
                    "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
                    "folder": "📸 Imagens"
                },
                "documents": {
                    "extensions": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
                    "folder": "📄 Documentos"
                },
                "audio": {
                    "extensions": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".wma"],
                    "folder": "🎵 Áudio"
                },
                "video": {
                    "extensions": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
                    "folder": "🎬 Vídeos"
                },
                "code": {
                    "extensions": [".py", ".js", ".html", ".css", ".cpp", ".c", ".java", ".php", ".rb", ".go", ".rs"],
                    "folder": "💻 Código"
                },
                "archives": {
                    "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
                    "folder": "📦 Arquivos Compactados"
                },
                "executables": {
                    "extensions": [".exe", ".msi", ".deb", ".rpm", ".dmg", ".app"],
                    "folder": "⚙️ Executáveis"
                }
            },
            "organize_by_date": False,
            "date_format": "%Y-%m",
            "watched_folders": [],
            "ignore_hidden": True,
            "create_subfolders": True
        }
        self.config = self.load_config()
        self.observer = None
        self.monitoring = False
        
    def load_config(self):
        """Carrega configurações do arquivo JSON"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Mescla com config padrão para adicionar novas opções
                merged_config = self.default_config.copy()
                merged_config.update(config)
                return merged_config
            except Exception as e:
                print(f"Erro ao carregar config: {e}")
        return self.default_config.copy()
    
    def save_config(self):
        """Salva configurações no arquivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar config: {e}")
    
    def get_file_category(self, file_path):
        """Determina a categoria do arquivo baseada na extensão"""
        extension = Path(file_path).suffix.lower()
        
        for category, rule in self.config["rules"].items():
            if extension in rule["extensions"]:
                return category, rule["folder"]
        
        return "outros", "📁 Outros"
    
    def organize_file(self, file_path, destination_folder, log_callback=None):
        """Organiza um arquivo específico"""
        try:
            if not os.path.isfile(file_path):
                return False, "Arquivo não encontrado"
            
            # Ignora arquivos ocultos se configurado
            if self.config.get("ignore_hidden", True) and Path(file_path).name.startswith('.'):
                return False, "Arquivo oculto ignorado"
            
            filename = os.path.basename(file_path)
            category, category_folder = self.get_file_category(file_path)
            
            # Determina pasta de destino
            if self.config.get("organize_by_date", False):
                file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                date_folder = file_date.strftime(self.config.get("date_format", "%Y-%m"))
                target_dir = os.path.join(destination_folder, date_folder, category_folder)
            else:
                target_dir = os.path.join(destination_folder, category_folder)
            
            # Cria diretório se não existir
            os.makedirs(target_dir, exist_ok=True)
            
            # Define caminho final
            target_path = os.path.join(target_dir, filename)
            
            # Resolve conflitos de nome
            counter = 1
            original_target = target_path
            while os.path.exists(target_path):
                name, ext = os.path.splitext(filename)
                target_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
                counter += 1
            
            # Move o arquivo
            shutil.move(file_path, target_path)
            
            message = f"✅ {filename} → {os.path.relpath(target_path, destination_folder)}"
            if log_callback:
                log_callback(message)
            
            return True, message
            
        except Exception as e:
            error_msg = f"❌ Erro ao mover {filename}: {str(e)}"
            if log_callback:
                log_callback(error_msg)
            return False, error_msg
    
    def organize_folder(self, folder_path, log_callback=None):
        """Organiza todos os arquivos de uma pasta"""
        if not os.path.exists(folder_path):
            return False, "Pasta não encontrada"
        
        organized_count = 0
        error_count = 0
        
        if log_callback:
            log_callback(f"🔄 Iniciando organização da pasta: {folder_path}")
        
        # Lista todos os arquivos
        for root, dirs, files in os.walk(folder_path):
            if root != folder_path:  # Evita organizar subpastas já organizadas
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                success, message = self.organize_file(file_path, folder_path, log_callback)
                if success:
                    organized_count += 1
                else:
                    error_count += 1
        
        summary = f"📊 Resumo: {organized_count} arquivos organizados, {error_count} erros"
        if log_callback:
            log_callback(summary)
        
        return True, summary

class FileWatcher(FileSystemEventHandler):
    """Handler para monitoramento de arquivos em tempo real"""
    
    def __init__(self, organizer, folder_path, log_callback=None):
        self.organizer = organizer
        self.folder_path = folder_path
        self.log_callback = log_callback
        
    def on_created(self, event):
        if not event.is_directory:
            # Pequeno delay para garantir que o arquivo foi completamente copiado
            time.sleep(1)
            if os.path.exists(event.src_path):
                self.organizer.organize_file(event.src_path, self.folder_path, self.log_callback)

class OrganizerGUI:
    def __init__(self):
        self.organizer = FileOrganizer()
        self.setup_gui()
        
    def setup_gui(self):
        """Configura a interface gráfica"""
        self.root = tk.Tk()
        self.root.title("🗂️ Organizador Automático de Arquivos")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuração de grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Seleção de pasta
        ttk.Label(main_frame, text="📁 Pasta para organizar:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0,5))
        
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0,10))
        folder_frame.columnconfigure(0, weight=1)
        
        self.folder_var = tk.StringVar()
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, font=("Arial", 10))
        self.folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0,5))
        
        ttk.Button(folder_frame, text="Procurar", command=self.select_folder).grid(row=0, column=1)
        
        # Botões principais
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0,10))
        
        ttk.Button(button_frame, text="🗂️ Organizar Agora", command=self.organize_now, 
                  style="Accent.TButton").pack(side=tk.LEFT, padx=(0,5))
        
        self.monitor_btn = ttk.Button(button_frame, text="👁️ Iniciar Monitoramento", command=self.toggle_monitoring)
        if WATCHDOG_AVAILABLE:
            self.monitor_btn.pack(side=tk.LEFT, padx=(0,5))
        
        ttk.Button(button_frame, text="⚙️ Configurações", command=self.show_config).pack(side=tk.LEFT, padx=(0,5))
        
        # Log
        ttk.Label(main_frame, text="📋 Log de atividades:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=(10,5))
        
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0,10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botões do log
        log_btn_frame = ttk.Frame(main_frame)
        log_btn_frame.grid(row=5, column=0, columnspan=2)
        
        ttk.Button(log_btn_frame, text="🗑️ Limpar Log", command=self.clear_log).pack(side=tk.LEFT, padx=(0,5))
        ttk.Button(log_btn_frame, text="💾 Salvar Log", command=self.save_log).pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Pronto para organizar")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10,0))
        
        # Configurações de redimensionamento
        main_frame.rowconfigure(4, weight=1)
        
        # Log inicial
        self.log("🚀 Organizador de Arquivos iniciado!")
        self.log("💡 Dica: Selecione uma pasta e clique em 'Organizar Agora'")
        
        if not WATCHDOG_AVAILABLE:
            self.log("⚠️ Watchdog não instalado. Monitoramento em tempo real indisponível.")
            self.log("   Para instalar: pip install watchdog")
    
    def log(self, message):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def select_folder(self):
        """Abre diálogo para seleção de pasta"""
        folder = filedialog.askdirectory(title="Selecione a pasta para organizar")
        if folder:
            self.folder_var.set(folder)
            self.log(f"📁 Pasta selecionada: {folder}")
    
    def organize_now(self):
        """Organiza a pasta selecionada"""
        folder = self.folder_var.get().strip()
        if not folder:
            messagebox.showwarning("Aviso", "Selecione uma pasta primeiro!")
            return
        
        if not os.path.exists(folder):
            messagebox.showerror("Erro", "Pasta não encontrada!")
            return
        
        self.status_var.set("Organizando...")
        self.log("=" * 50)
        
        # Executa organização em thread separada
        def organize_thread():
            try:
                success, message = self.organizer.organize_folder(folder, self.log)
                self.root.after(0, lambda: self.status_var.set("Organização concluída!"))
                if success:
                    self.root.after(0, lambda: messagebox.showinfo("Sucesso", "Organização concluída!"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro na organização: {e}"))
                self.root.after(0, lambda: self.status_var.set("Erro na organização"))
        
        Thread(target=organize_thread, daemon=True).start()
    
    def toggle_monitoring(self):
        """Inicia/para o monitoramento em tempo real"""
        if not WATCHDOG_AVAILABLE:
            messagebox.showerror("Erro", "Watchdog não está instalado!")
            return
            
        folder = self.folder_var.get().strip()
        if not folder:
            messagebox.showwarning("Aviso", "Selecione uma pasta primeiro!")
            return
        
        if not self.organizer.monitoring:
            # Inicia monitoramento
            try:
                event_handler = FileWatcher(self.organizer, folder, self.log)
                self.organizer.observer = Observer()
                self.organizer.observer.schedule(event_handler, folder, recursive=False)
                self.organizer.observer.start()
                self.organizer.monitoring = True
                
                self.monitor_btn.config(text="⏸️ Parar Monitoramento")
                self.status_var.set(f"Monitorando: {folder}")
                self.log(f"👁️ Monitoramento iniciado em: {folder}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao iniciar monitoramento: {e}")
        else:
            # Para monitoramento
            if self.organizer.observer:
                self.organizer.observer.stop()
                self.organizer.observer.join()
            
            self.organizer.monitoring = False
            self.monitor_btn.config(text="👁️ Iniciar Monitoramento")
            self.status_var.set("Monitoramento parado")
            self.log("⏸️ Monitoramento parado")
    
    def show_config(self):
        """Mostra janela de configurações"""
        ConfigWindow(self.organizer, self.log)
    
    def clear_log(self):
        """Limpa o log"""
        self.log_text.delete(1.0, tk.END)
        self.log("🗑️ Log limpo")
    
    def save_log(self):
        """Salva o log em arquivo"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
            )
            if filename:
                content = self.log_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log(f"💾 Log salvo em: {filename}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar log: {e}")
    
    def on_closing(self):
        """Handler para fechamento da aplicação"""
        if self.organizer.monitoring and self.organizer.observer:
            self.organizer.observer.stop()
            self.organizer.observer.join()
        self.root.destroy()
    
    def run(self):
        """Executa a aplicação"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

class ConfigWindow:
    """Janela de configurações"""
    
    def __init__(self, organizer, log_callback):
        self.organizer = organizer
        self.log_callback = log_callback
        self.setup_window()
    
    def setup_window(self):
        """Configura a janela de configurações"""
        self.window = tk.Toplevel()
        self.window.title("⚙️ Configurações")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba de regras
        rules_frame = ttk.Frame(notebook)
        notebook.add(rules_frame, text="📋 Regras de Organização")
        self.setup_rules_tab(rules_frame)
        
        # Aba de opções
        options_frame = ttk.Frame(notebook)
        notebook.add(options_frame, text="⚙️ Opções Gerais")
        self.setup_options_tab(options_frame)
        
        # Botões
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="💾 Salvar", command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 Resetar", command=self.reset_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
    
    def setup_rules_tab(self, parent):
        """Configura a aba de regras"""
        # Lista de regras
        ttk.Label(parent, text="Regras de organização por tipo de arquivo:", font=("Arial", 10, "bold")).pack(pady=(10,5))
        
        rules_text = scrolledtext.ScrolledText(parent, height=20, font=("Consolas", 9))
        rules_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Mostra regras atuais
        rules_content = json.dumps(self.organizer.config["rules"], indent=2, ensure_ascii=False)
        rules_text.insert(tk.END, rules_content)
        
        self.rules_text = rules_text
        
        ttk.Label(parent, text="💡 Edite o JSON acima para personalizar as regras", 
                 font=("Arial", 9)).pack(pady=5)
    
    def setup_options_tab(self, parent):
        """Configura a aba de opções"""
        # Organizar por data
        self.date_var = tk.BooleanVar(value=self.organizer.config.get("organize_by_date", False))
        ttk.Checkbutton(parent, text="📅 Organizar arquivos por data", 
                       variable=self.date_var).pack(anchor=tk.W, padx=10, pady=5)
        
        # Formato de data
        ttk.Label(parent, text="Formato da data:").pack(anchor=tk.W, padx=10, pady=(10,0))
        self.date_format_var = tk.StringVar(value=self.organizer.config.get("date_format", "%Y-%m"))
        ttk.Entry(parent, textvariable=self.date_format_var, width=20).pack(anchor=tk.W, padx=10, pady=5)
        
        # Ignorar arquivos ocultos
        self.hidden_var = tk.BooleanVar(value=self.organizer.config.get("ignore_hidden", True))
        ttk.Checkbutton(parent, text="👁️ Ignorar arquivos ocultos (que começam com .)", 
                       variable=self.hidden_var).pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Label(parent, text="\n📝 Formatos de data disponíveis:", font=("Arial", 9, "bold")).pack(anchor=tk.W, padx=10)
        ttk.Label(parent, text="%Y-%m = 2025-08 (ano-mês)", font=("Arial", 8)).pack(anchor=tk.W, padx=20)
        ttk.Label(parent, text="%Y-%m-%d = 2025-08-24 (ano-mês-dia)", font=("Arial", 8)).pack(anchor=tk.W, padx=20)
        ttk.Label(parent, text="%Y = 2025 (apenas ano)", font=("Arial", 8)).pack(anchor=tk.W, padx=20)
    
    def save_config(self):
        """Salva as configurações"""
        try:
            # Salva regras
            rules_content = self.rules_text.get(1.0, tk.END).strip()
            new_rules = json.loads(rules_content)
            self.organizer.config["rules"] = new_rules
            
            # Salva opções
            self.organizer.config["organize_by_date"] = self.date_var.get()
            self.organizer.config["date_format"] = self.date_format_var.get()
            self.organizer.config["ignore_hidden"] = self.hidden_var.get()
            
            # Salva arquivo
            self.organizer.save_config()
            
            self.log_callback("⚙️ Configurações salvas com sucesso!")
            messagebox.showinfo("Sucesso", "Configurações salvas!")
            self.window.destroy()
            
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "Erro no formato JSON das regras!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
    
    def reset_config(self):
        """Reseta configurações para o padrão"""
        if messagebox.askyesno("Confirmar", "Resetar todas as configurações?"):
            self.organizer.config = self.organizer.default_config.copy()
            self.organizer.save_config()
            self.log_callback("🔄 Configurações resetadas para o padrão")
            messagebox.showinfo("Sucesso", "Configurações resetadas!")
            self.window.destroy()

def main():
    """Função principal"""
    try:
        app = OrganizerGUI()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")

if __name__ == "__main__":
    main()
