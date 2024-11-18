import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import ConnectionPatch
from matplotlib.gridspec import GridSpec

def is_prime(n):
    """Optimized primality test."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(np.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def find_goldbach_pairs(n):
    """Find all prime pairs that sum to n."""
    pairs = []
    for i in range(2, n//2 + 1):
        if is_prime(i) and is_prime(n-i):
            pairs.append((i, n-i))
    return pairs

def create_visualization(n, pairs):
    """Create an multi-plot visualization of Goldbach pairs."""
    
    pairs = np.array(pairs)
    first_primes = pairs[:, 0]
    second_primes = pairs[:, 1]

    fig = plt.figure(figsize=(15, 12))
    gs = GridSpec(3, 3, figure=fig)
    
    ax_scatter = fig.add_subplot(gs[1:, :2])
    scatter = ax_scatter.scatter(first_primes, second_primes, 
                               c=first_primes + second_primes,
                               cmap='viridis', s=100, alpha=0.6)
    ax_scatter.set_xlabel('First Prime', fontsize=12)
    ax_scatter.set_ylabel('Second Prime', fontsize=12)
    ax_scatter.set_title(f'Prime Pairs Distribution for {n}', fontsize=14)
    ax_scatter.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax_scatter, label='Sum')
    
    ax_scatter.plot([0, n], [n, 0], 'r--', alpha=0.5, label=f'Sum = {n}')
    ax_scatter.legend()
    
    
    ax_hist_top = fig.add_subplot(gs[0, :2])
    sns.histplot(data=first_primes, bins=min(30, len(first_primes)), 
                ax=ax_hist_top, color='blue', alpha=0.6)
    ax_hist_top.set_title('Distribution of First Primes', fontsize=12)
    ax_hist_top.set_xlabel('')
    
    ax_hist_right = fig.add_subplot(gs[1:, 2])
    sns.histplot(data=second_primes, bins=min(30, len(second_primes)), 
                ax=ax_hist_right, color='green', alpha=0.6, orientation='horizontal')
    ax_hist_right.set_title('Distribution of\nSecond Primes', fontsize=12)
    ax_hist_right.set_ylabel('')

    ax_summary = fig.add_subplot(gs[0, 2])
    ax_summary.axis('off')
    summary_text = (
        f"Summary Statistics\n\n"
        f"Total Pairs: {len(pairs)}\n"
        f"Min First Prime: {min(first_primes)}\n"
        f"Max First Prime: {max(first_primes)}\n"
        f"Min Second Prime: {min(second_primes)}\n"
        f"Max Second Prime: {max(second_primes)}\n"
        f"Most Common First: {np.bincount(first_primes.astype(int)).argmax()}\n"
        f"Most Common Second: {np.bincount(second_primes.astype(int)).argmax()}"
    )
    ax_summary.text(0.05, 0.95, summary_text, 
                   transform=ax_summary.transAxes,
                   verticalalignment='top',
                   fontfamily='monospace',
                   fontsize=10)
    

    for i in range(min(5, len(pairs))):  
        con1 = ConnectionPatch(
            xyA=(first_primes[i], second_primes[i]), coordsA=ax_scatter.transData,
            xyB=(first_primes[i], 0), coordsB=ax_hist_top.transData,
            color='gray', alpha=0.2
        )
        fig.add_artist(con1)
        
  
        con2 = ConnectionPatch(
            xyA=(first_primes[i], second_primes[i]), coordsA=ax_scatter.transData,
            xyB=(0, second_primes[i]), coordsB=ax_hist_right.transData,
            color='gray', alpha=0.2
        )
        fig.add_artist(con2)
    
 
    print(f"\nGoldbach Pairs for {n}:")
    for p1, p2 in pairs:
        print(f"{p1:4d} + {p2:4d} = {n}")
    
    plt.tight_layout()
    plt.show()

def main():
    print("Enhanced Goldbach Conjecture Visualization")
    print("=========================================")
    
    while True:
        try:
            n = int(input("\nEnter an even number (≥ 4): "))
            if n < 4:
                print("Please enter a number greater than or equal to 4.")
                continue
            if n % 2 != 0:
                print("Please enter an even number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nFinding prime pairs for {n}...")
    pairs = find_goldbach_pairs(n)
    
    if pairs:
        print(f"Found {len(pairs)} prime pairs!")
        create_visualization(n, pairs)
    else:
        print("No prime pairs found! This would disprove the Goldbach Conjecture!")

if __name__ == "__main__":
    main()