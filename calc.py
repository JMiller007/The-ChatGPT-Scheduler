from collections import deque

def opt_page_faults(reference_string, frame_size):
    frame_set = set()
    page_faults = 0

    for i, page in enumerate(reference_string):
        if page not in frame_set:
            if len(frame_set) < frame_size:
                frame_set.add(page)
            else:
                future_pages = reference_string[i+1:]
                pages_in_frames = list(frame_set)
                pages_to_replace = set(pages_in_frames)

                for future_page in future_pages:
                    if future_page in pages_in_frames:
                        pages_to_replace.discard(future_page)
                        if len(pages_to_replace) == 0:
                            break

                page_to_replace = pages_in_frames.index(pages_to_replace.pop())
                frame_set.remove(pages_in_frames[page_to_replace])
                frame_set.add(page)
                page_faults += 1

    return page_faults


def fifo_page_faults(reference_string, frame_size):
    frame_queue = deque(maxlen=frame_size)
    page_faults = 0

    for page in reference_string:
        if page not in frame_queue:
            frame_queue.append(page)
            page_faults += 1

    return page_faults

def lru_page_faults(reference_string, frame_size):
    frame_set = set()
    frame_list = []
    page_faults = 0

    for page in reference_string:
        if page not in frame_set:
            if len(frame_set) < frame_size:
                frame_set.add(page)
                frame_list.append(page)
            else:
                least_recently_used = frame_list.pop(0)
                frame_set.remove(least_recently_used)
                frame_set.add(page)
                frame_list.append(page)
            page_faults += 1
        else:
            frame_list.remove(page)
            frame_list.append(page)

    return page_faults

# Example usage:
reference_string = [1, 2, 3, 10, 20, 30, 40, 1, 2, 1, 2, 30, 40, 10, 1, 2, 3, 10, 20]
frame_size = 5

opt_faults = opt_page_faults(reference_string, frame_size)
fifo_faults = fifo_page_faults(reference_string, frame_size)
lru_faults = lru_page_faults(reference_string, frame_size)

print(f"Page Fault Count for OPT: {opt_faults}")
print(f"Page Fault Count for FIFO: {fifo_faults}")
print(f"Page Fault Count for LRU: {lru_faults}")
