import time
import os
from datetime import datetime, timedelta
from typing import Optional


class FocusSession:
    """Represents a single focus session."""
    
    def __init__(self, work_duration: int, break_duration: int, sessions: int = 4):
        self.work_duration = work_duration  # in seconds
        self.break_duration = break_duration  # in seconds
        self.sessions = sessions  # number of full cycles before long break
        self.current_session = 0
        self.total_focus_time = 0
        self.session_start = None
        self.is_running = False
    
    def format_time(self, seconds: int) -> str:
        """Convert seconds to MM:SS format."""
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display_timer(self, remaining: int, phase: str):
        """Display the timer with progress bar."""
        self.clear_screen()
        print("=" * 50)
        print("         DAILY FOCUS TIMER - POMODORO STYLE")
        print("=" * 50)
        print()
        
        # Session info
        cycle = (self.current_session // 2) + 1
        print(f"Cycle: {cycle} | Total Focus Time: {self.format_time(self.total_focus_time)}")
        print()
        
        # Phase and timer
        total = self.work_duration if phase == "WORK" else self.break_duration
        progress = total - remaining
        percentage = (progress / total) * 100
        
        print(f"Phase: {phase}")
        print(f"Time: {self.format_time(remaining)}")
        print()
        
        # Progress bar
        bar_length = 40
        filled = int(bar_length * percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"Progress: [{bar}] {percentage:.0f}%")
        print()
        print("Press Ctrl+C to skip this session")
        print("=" * 50)
    
    def play_notification(self):
        """Play a terminal bell notification."""
        print('\a')  # Terminal bell
        print('\a')  # Double bell for emphasis
    
    def run_phase(self, phase: str, duration: int):
        """Run a single timer phase."""
        start_time = time.time()
        
        try:
            while True:
                elapsed = int(time.time() - start_time)
                remaining = duration - elapsed
                
                if remaining <= 0:
                    break
                
                self.display_timer(remaining, phase)
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\nPhase skipped!")
            time.sleep(1)
            return False
        
        # Phase completed
        self.play_notification()
        print(f"\n{phase} phase complete! 🎉")
        time.sleep(2)
        return True
    
    def run(self):
        """Run the full focus session."""
        self.is_running = True
        session_num = 0
        
        try:
            while session_num < self.sessions:
                # Work phase
                print(f"\nStarting work session {session_num + 1} of {self.sessions}...")
                time.sleep(2)
                
                if self.run_phase("WORK", self.work_duration):
                    self.total_focus_time += self.work_duration
                    self.current_session += 1
                    session_num += 1
                
                # Don't add break after last session
                if session_num < self.sessions:
                    # Short break
                    print(f"\nTake a short break!")
                    time.sleep(2)
                    self.run_phase("BREAK", self.break_duration)
                    self.current_session += 1
            
            # Final summary
            self.display_summary()
        
        except KeyboardInterrupt:
            print("\n\nTimer interrupted. Session saved.")
            self.display_summary()
        
        finally:
            self.is_running = False
    
    def display_summary(self):
        """Display session summary."""
        self.clear_screen()
        print("=" * 50)
        print("           DAILY FOCUS TIMER - SUMMARY")
        print("=" * 50)
        print()
        print(f"Total Focus Time: {self.format_time(self.total_focus_time)}")
        print(f"Sessions Completed: {self.current_session // 2}")
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("Great work! Stay focused! 💪")
        print("=" * 50)


def get_user_preferences() -> tuple[int, int, int]:
    """Get user preferences for timer settings."""
    print("=" * 50)
    print("      DAILY FOCUS TIMER - CONFIGURATION")
    print("=" * 50)
    print()
    
    while True:
        try:
            work = int(input("Work duration in minutes (default 25): ") or 25)
            if work <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        try:
            break_time = int(input("Break duration in minutes (default 5): ") or 5)
            if break_time <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        try:
            sessions = int(input("Number of sessions (default 4): ") or 4)
            if sessions <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    return work * 60, break_time * 60, sessions


def main():
    """Main entry point."""
    print("\n🎯 Welcome to Daily Focus Timer!\n")
    
    # Get preferences
    work_duration, break_duration, num_sessions = get_user_preferences()
    
    # Create and run session
    session = FocusSession(work_duration, break_duration, num_sessions)
    
    print(f"\nStarting timer in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"{i}...", end=" ", flush=True)
        time.sleep(1)
    print()
    
    session.run()


if __name__ == "__main__":
    main()
