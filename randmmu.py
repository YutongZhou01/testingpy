from mmu import MMU
import random

class RandMMU(MMU):
    def __init__(self, frames):
        self.buffer_size = frames
        self.frames = [{'page_number': None, 'modify-bit': 0} for i in range(frames)] # Initialize with dictionaries
        self.reads = 0
        self.writes = 0
        self.page_faults = 0
        self.debug = False

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def read_memory(self, page_number):
        self.reads += 1
        # if page_number is not in frames, page fault
        if not any(frame['page_number'] == page_number for frame in self.frames): 
            if self.debug:
                print(f"Page fault".ljust(15) + f"{page_number}")
            self.page_faults += 1 
            # Buffer is not full
            if len(self.frames) != self.buffer_size: 
                if self.debug:
                    print(f"Reading".ljust(15) + f"{page_number}")
                self.frames.insert(0, {'page_number': page_number, 'modify-bit': 0})
            # Buffer is full
            else: 
                replacement = random.randint(0, len(self.frames) - 1) # Randomly select a frame to replace
                if self.frames[replacement]['modify-bit'] == 1: # Only write if the page was modified
                    self.writes += 1
                    if self.debug:
                        print(f"Disk write".ljust(15) + f"{self.frames[replacement]['page_number']}")
                if self.debug:
                    print(f"Reading".ljust(15) + f"{page_number}")
                self.frames[replacement] = {'page_number': page_number, 'modify-bit': 0}
        # if page_number is in frames, do nothing
        else:
            if self.debug:
                print(f"Reading".ljust(15) + f"{page_number}")

    def write_memory(self, page_number):
        self.reads += 1
        # if page_number is not in frames, page fault
        if not any(frame['page_number'] == page_number for frame in self.frames):
            if self.debug:
                print(f"Page fault".ljust(15) + f"{page_number}")
            self.page_faults += 1 
            if len(self.frames) != self.buffer_size: # Buffer is not full
                if self.debug:
                    print(f"Writing".ljust(15) + f"{page_number}")
                self.frames.insert(0, {'page_number': page_number, 'modify-bit': 1})
            # Buffer is full
            else: 
                replacement = random.randint(0, len(self.frames) - 1) # Randomly select a frame to replace
                if self.frames[replacement]['modify-bit'] == 1: # Only write if the page was modified
                    self.writes += 1
                    if self.debug:
                        print(f"Disk write".ljust(15) + f"{self.frames[replacement]['page_number']}")
                if self.debug:
                    print(f"Writing".ljust(15) + f"{page_number}")
                self.frames[replacement] = {'page_number': page_number, 'modify-bit': 1}
        # if page_number is in frames, set modify-bit to 1
        else:
            frame = next(frame for frame in self.frames if frame['page_number'] == page_number)
            frame['modify-bit'] = 1
            if self.debug:
                print(f"Writing".ljust(15) + f"{page_number}")

    def get_total_disk_reads(self):
        return self.reads

    def get_total_disk_writes(self):
        return self.writes

    def get_total_page_faults(self):
        return self.page_faults
    
    def get_frames(self):
        return self.frames
