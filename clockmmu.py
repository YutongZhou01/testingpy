from mmu import MMU

class ClockMMU(MMU):
    def __init__(self, frames):
        self.num_frames = frames
        self.frames = [{'page_number': None, 'use-bit': 0, 'modify-bit': 0} for i in range(frames)] # initialize frames with page_number and use-bit using a dictionary sttructure
        self.clock_hand = 0 # initialize clock hand to 0
        self.reads = 0
        self.writes = 0
        self.page_faults = 0
        self.debug = False

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False 

    # Increment the clock hand
    def clock_tick(self):
        self.clock_hand = (self.clock_hand + 1) % self.num_frames # clock hand will loop back to 0 if it reaches the end of the frames
        # if self.debug:
        #     print(f"Clock tick".ljust(15) + f"{self.clock_hand}")

    # Clock replacement algorithm
    def clock_replace(self, page_number, mode):
        while True:
            # if use-bit is 0, replace page, set clock bit to 1, and clock tick
            if self.frames[self.clock_hand]['use-bit'] == 0:       
                # If modify-bit is set, increment disk writes
                if self.frames[self.clock_hand]['modify-bit'] == 1:
                    self.writes += 1
                    if self.debug:
                        print(f"Disk write".ljust(15) + f"{self.frames[self.clock_hand]['page_number']}")    
                self.reads += 1 # Always increment reads for a page fault
                self.frames[self.clock_hand]['page_number'] = page_number
                self.frames[self.clock_hand]['use-bit'] = 1
                self.frames[self.clock_hand]['modify-bit'] = 1 if mode == 'write' else 0 # Set modify-bit to 1 if mode is write, else 0
                self.clock_tick()
                break
            # if use-bit is 1, set use-bit to 0 and clock tick
            else:
                self.frames[self.clock_hand]['use-bit'] = 0
                self.clock_tick()



    def read_memory(self, page_number):
        # if page_number is not in frames, page fault
        if not any(frame['page_number'] == page_number for frame in self.frames):
            if self.debug:
                print(f"Page fault".ljust(15) + f"{page_number}")
            self.page_faults += 1     
            self.clock_replace(page_number, mode='read')
        # if page_number is in frames, set use-bit to 1
        else:
            if self.debug:
                print(f"Reading".ljust(15) + f"{page_number}")        
            index = next(i for i, frame in enumerate(self.frames) if frame['page_number'] == page_number) # loop through frames to find page_number and set use-bit to 1
            self.frames[index]['use-bit'] = 1

    def write_memory(self, page_number): 
        # if page_number is not in frames, page fault
        if not any(frame['page_number'] == page_number for frame in self.frames):
            if self.debug:
                print(f"Page fault".ljust(15) + f"{page_number}")
            self.page_faults += 1
            self.clock_replace(page_number, mode='write')
        # if page_number is in frames, set use-bit and modify-bit to 1
        else:
            if self.debug:
                print(f"Writing".ljust(15) + f"{page_number}")
            index = next(i for i, frame in enumerate(self.frames) if frame['page_number'] == page_number) # loop through frames to find page_number and set use-bit to 1
            self.frames[index]['use-bit'] = 1
            self.frames[index]['modify-bit'] = 1 

    def get_total_disk_reads(self):
        return self.reads

    def get_total_disk_writes(self):
        return self.writes
    
    def get_total_page_faults(self):
        return self.page_faults
