from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        self.buffer_size = frames
        self.frames = [{'page_number': None, 'modify-bit': 0} for i in range(frames)] # added modify-bit to keep track of disk writes
        self.reads = 0 
        self.writes = 0
        self.page_faults = 0
        self.debug = False

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False
    
    def read_memory(self, page_number):
            
        # Check if the page is already in frames, if not, page fault
        if not any(frame['page_number'] == page_number for frame in self.frames):
            if self.debug:
                print(f"Page fault".ljust(15) + f"{page_number}") 
            self.page_faults += 1
            self.reads += 1
            # If buffer isn't full yet, add the page
            if len(self.frames) < self.buffer_size: 
                if self.debug:
                    print(f"Reading".ljust(15) + f"{page_number}")
                self.frames.insert(0, {'page_number': page_number, 'modify-bit': 0})
            else: 
                # If the last frame (to be replaced) is modified, incrementt writes
                if self.frames[-1]['modify-bit'] == 1:
                    self.writes += 1
                    if self.debug:
                        print(f"Disk write".ljust(15) + f"{self.frames[-1]['page_number']}")
                if self.debug:
                    print(f"Reading".ljust(15) + f"{page_number}")
                self.frames.pop()  # Remove the least recently used page (last element)
                self.frames.insert(0, {'page_number': page_number, 'modify-bit': 0})
        else:
            # If the page is already in frames, move it to the front (most recently used position)
            frame = next(frame for frame in self.frames if frame['page_number'] == page_number)
            self.frames.remove(frame)
            if self.debug:
                print(f"Reading".ljust(15) + f"{page_number}")
            self.frames.insert(0, frame)  # The modify bit remains unchanged

    def write_memory(self, page_number):    
        # Check if the page is already in frames, if not, page fault
        if not any(frame['page_number'] == page_number for frame in self.frames):
            if self.debug:
                print(f"Page fault".ljust(15) + f"{page_number}") 
            self.page_faults += 1
            self.reads += 1  # Increment disk read due to page fault

            # If buffer isn't full yet, add the page and mark it as modified
            if len(self.frames) < self.buffer_size: 
                if self.debug:
                    print(f"Writing".ljust(15) + f"{page_number}")
                self.frames.insert(0, {'page_number': page_number, 'modify-bit': 1})
            else: 
                # If the last frame (to be replaced) is modified, increment writes
                if self.frames[-1]['modify-bit'] == 1:
                    self.writes += 1
                    if self.debug:
                        print(f"Disk write".ljust(15) + f"{self.frames[-1]['page_number']}")
                if self.debug:
                    print(f"Writing".ljust(15) + f"{page_number}")
                self.frames.pop()  # Remove the least recently used page
                self.frames.insert(0, {'page_number': page_number, 'modify-bit': 1})
        else:
            # If the page is already in frames, mark it as modified and move to the front
            frame = next(frame for frame in self.frames if frame['page_number'] == page_number)
            frame['modify-bit'] = 1
            self.frames.remove(frame)
            if self.debug:
                print(f"Writing".ljust(15) + f"{page_number}")
            self.frames.insert(0, frame)


    def get_total_disk_reads(self):
        return self.reads   

    def get_total_disk_writes(self):
        return self.writes  

    def get_total_page_faults(self):
        return self.page_faults

    def get_frames(self):
        return self.frames