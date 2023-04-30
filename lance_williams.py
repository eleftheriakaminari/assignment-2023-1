import sys
# Διαβάζω δεδομένα απο τα αρχείο
def read_data(filename):

     data = []
     with open(filename, 'r') as f:
        for line in f:
            data.append(list(map(float, line.strip().split())))
        return data


def print_cluster(cluster, distance, size):
    if len(cluster) == 1:
        print(f"({int(cluster[0])}) {distance:.2f} {size}")
    else:
        print(f"({','.join(map(str, map(int, cluster)))}) {distance:.2f} {size}")

# hierarchical clustering με βάση μελέτη Lance-Williams algorithm
def lance_williams(data, linkage):
    clusters = [[i] for i in range(len(data))]
    distances = {}
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            distances[(i, j)] = linkage(data, clusters[i], clusters[j])
    # ευρευση μοναδικότητας
    for k in range(len(clusters), 1, -1):
        i, j = min(distances, key=distances.get)
        cluster_i, cluster_j = clusters[i], clusters[j]
        distance = distances.pop((i, j))
        size = len(cluster_i) + len(cluster_j)
        new_cluster = cluster_i + cluster_j
        clusters.pop(j)
        clusters[i] = new_cluster
        #περναω αποστάσεις σε νεο cluster (kanv update)
        for l in range(len(clusters)):
            if l != i:
                if (l, i) in distances:
                    distances[(l, i)] = linkage(data, clusters[l], new_cluster)
                else:
                    distances[(i, l)] = linkage(data, new_cluster, clusters[l])
        print_cluster(cluster_i, distance / 2, len(cluster_i))
        print_cluster(cluster_j, distance / 2, len(cluster_j))
        print_cluster(new_cluster, 0.0, size)

def single_linkage(data, cluster1, cluster2):
    min_distance = sys.float_info.max
    for i in cluster1:
        for j in cluster2:
            distance = ((data[i][0] - data[j][0]) ** 2 + (data[i][1] - data[j][1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
    return min_distance
# main

if __name__ == '__main__':
    linkage_methods = {'single': single_linkage}
    linkage_method = linkage_methods[sys.argv[1]]
    data = read_data(sys.argv[2])
    lance_williams(data, linkage_method)
