#!/usr/bin/env python3

import os
import time
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo
import threading

# Set up logging
def setup_logging():
    logger = logging.getLogger('auto_commit')
    logger.setLevel(logging.INFO)
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Rotating file handler - keeps 1 backup file of 1MB each
    handler = RotatingFileHandler(
        'logs/auto_commit.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=1
    )
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)
    
    return logger

class GitAutoCommitHandler(FileSystemEventHandler):
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        self.last_change_time = time.time()
        self.commit_timer = None
        self.commit_delay = 600  # 10 minutes in seconds
        self.lock = threading.Lock()
        self.logger = setup_logging()

    def on_any_event(self, event):
        if not event.is_directory and not event.src_path.endswith('.log') and '.git' not in event.src_path:
            with self.lock:
                self.last_change_time = time.time()
                if self.commit_timer:
                    self.commit_timer.cancel()
                self.commit_timer = threading.Timer(self.commit_delay, self.commit_changes)
                self.commit_timer.start()
                self.logger.info(f"Change detected: {event.src_path}")

    def commit_changes(self):
        try:
            with self.lock:
                if time.time() - self.last_change_time >= self.commit_delay:
                    self.repo.git.add(all=True)
                    if self.repo.index.diff('HEAD'):
                        commit_message = f"Auto commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        self.repo.index.commit(commit_message)
                        self.repo.remotes.origin.push()
                        self.logger.info(f"Changes committed and pushed at {datetime.now()}")
        except Exception as e:
            self.logger.error(f"Error during auto commit: {str(e)}")

def main():
    # Get the repository path (current directory)
    repo_path = os.getcwd()
    
    # Initialize the event handler
    event_handler = GitAutoCommitHandler(repo_path)
    
    # Initialize the observer
    observer = Observer()
    observer.schedule(event_handler, repo_path, recursive=True)
    
    # Start the observer
    observer.start()
    event_handler.logger.info(f"Started monitoring {repo_path} for changes...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.commit_timer:
            event_handler.commit_timer.cancel()
        event_handler.logger.info("Stopping auto commit daemon...")
    observer.join()

if __name__ == "__main__":
    main() 