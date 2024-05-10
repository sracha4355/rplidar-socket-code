import numpy as np
import matplotlib.pyplot as plt

class DBSCAN:
    def __init__(self, eps=0.5, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples

    def fit(self, data):
        self.visited = set()
        self.cluster_labels = np.zeros(len(data), dtype=int)
        self.cluster_id = 0

        for i in range(len(data)):
            if i in self.visited:
                continue

            neighbors = self._find_neighbors(data, i)
            if len(neighbors) < self.min_samples:
                self.cluster_labels[i] = -1  # Mark as noise
            else:
                self._expand_cluster(data, i, neighbors)
                self.cluster_id += 1

        return self.cluster_labels

    def _find_neighbors(self, data, idx):
        neighbors = []
        for i in range(len(data)):
            if np.linalg.norm(data[i] - data[idx]) < self.eps:
                neighbors.append(i)
        return neighbors

    def _expand_cluster(self, data, idx, neighbors):
        self.cluster_labels[idx] = self.cluster_id
        self.visited.add(idx)

        while neighbors:
            current_point = neighbors.pop(0)
            if current_point not in self.visited:
                self.visited.add(current_point)
                new_neighbors = self._find_neighbors(data, current_point)
                if len(new_neighbors) >= self.min_samples:
                    neighbors.extend(new_neighbors)
            if self.cluster_labels[current_point] == 0:
                self.cluster_labels[current_point] = self.cluster_id

def visualize_clusters(data, labels):
    unique_labels = np.unique(labels)
    colors = plt.cm.Spectral(np.linspace(0.4, 1, len(unique_labels)))

    plt.figure(figsize=(8, 6))
    for i, label in enumerate(unique_labels):
        if label == -1:
            cluster_data = data[labels == label]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], color='gray', alpha=0.5, label='Noise')
        else:
            cluster_data = data[labels == label]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], color=colors[i], alpha=0.5, label=f'Cluster {label}')
    plt.title('DBSCAN Clustering')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()
# Example usage
if __name__ == "__main__":
    # Generate random data
    np.random.seed(0)
    #data = np.random.randn(100, 2)
    from polar_plo import combined
    data = np.array(combined)

    # Initialize and fit DBSCAN model
    dbscan = DBSCAN(eps=5, min_samples=8)
    labels = dbscan.fit(data)

    # Visualize clusters
    visualize_clusters(data, labels)
