import asyncio
import multiprocessing as mp
import time
import random

async def process_data(data):
    """An example asynchronous data processing task"""
    await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate I/O bound work
    return data.upper()  # A simple data manipulation

async def process_chunk_async(chunk):
    """Process a chunk of data within the asyncio event loop"""
    results = await asyncio.gather(*[process_data(item) for item in chunk]) 
    #*[...] (Unpacking the List)<coroutine object process_data at ...>, <coroutine object process_data at ...>, <coroutine object process_data at ...>
    return results


def process_chunk_sync(chunk):
    """Wrapper to run async task in synchronous function"""
    return asyncio.run(process_chunk_async(chunk))


def main():
    num_processes = 3
    data = [f"item_{i}" for i in range(200)]
    chunk_size = len(data) // num_processes
    data_chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    start_time = time.time()
    
    with mp.Pool(processes=num_processes) as pool:
        results = pool.map(process_chunk_sync, data_chunks)
    end_time = time.time()

    flat_results = [item for sublist in results for item in sublist]
    print(f"Processed {len(flat_results)} items in {end_time-start_time:.2f} seconds")
    #for i in flat_results:
        #print(i)
    
    

if __name__ == "__main__":
    main()