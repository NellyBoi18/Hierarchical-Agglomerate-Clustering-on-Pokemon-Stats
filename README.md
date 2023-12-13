# Hierarchical Agglomerate Clustering on Pokemon Stats

This program performs hierarchical clustering on publicly available Pokemon stats. Each Poke mon is defined by a row in the data set. Because there are various ways to characterize how strong a Pokemon is, we summarize the stats into a shorter feature vector. We represent a Pokemon’s quality by 6 numbers:

```
HP, Attack, Defense, Sp. Atk, Sp. Def, Speed
```
After each Pokemon is represented as a 6 -dimensional feature vector(x<sub>1</sub>, ..., x<sub>6</sub>), we cluster the first *n* Pokemon with hierarchical agglomerate clustering (HAC). The function should work similarly to **scipy.cluster.hierarchy.linkage()** with **method='complete'**.

## Program Overview

The data in CSV format can be found in the file Pokemon.csv. Here is a high level description
of each function:

1. **load_data(filepath)** — takes in a string with a path to a CSV file, and returns the
    data points as a list of dicts.
2. **calc_features(row)** — takes in one row dict from the data loaded from the previous
    function then calculates the corresponding feature vector for that Pokemon as specified
    above, and returns it as anumpy array of shape(6,). The dtype of this array should
    beint64
3. **hac(features)** — performs complete linkage hierarchical agglomerate clustering on
    the Pokemon with the(x<sub>1</sub>, ..., x<sub>6</sub>) feature representation, and returns a numpy array
    representing the clustering.
4. **imshow_hac(Z)** — visualizes the hierarchical agglomerate clustering on the Pokemon’s
    feature representation.

## Program Details

### 1) load_data(filepath)

Summary:

- Input: string, the path to a file to be read.
- Output: list; each element of thelistis a dictrepresenting one row of the file
    read; the key ofdictis astring(such as ‘Attack’) and the value of thestringis a
    string(such as ‘111’).

Details:

1. Readin the file specified in the argument, filepath.
2. Return a list of dictionaries, where each row in the dataset is a dictionary with
    the column headers as keys and the row elements as values. The keys are strings:
    ‘HP’, ‘Attack’, ‘Defense’, ‘Sp. Atk’, ‘Sp. Def’, ‘Speed’.

```
You may assume the file exists and is a properly formatted CSV.
```
### 2) calc_features(row)

Summary:

- Input: dict representing one Pokemon.
- Output: numpy array of shape (6,) and dtype int64. The first element is x<sub>1</sub> and so
    on with the sixth element being x<sub>6</sub>.


Details: This function takes as input the dict representing one Pokemon, and computes
the feature representation (x<sub>1</sub>, ..., x<sub>6</sub>). Specifically,

1. *x<sub>1</sub>* = Attack
2. *x<sub>2</sub>* = Sp. Attack
3. *x<sub>3</sub>* = Speed
4. *x<sub>4</sub>* = Defense
5. *x<sub>5</sub>* = Sp. Def
6. *x<sub>6</sub>* = HP

Note, these stats in the dict would be string. We convert each relevant stat
to int when computing each x<sub>i</sub>. Return a numpy arrayhaving eachxiin order:x 1 ,... , x 6.
The shape of this array is (6,). The dtype of this array is int64. This function works for only one Pokemon at a time, not all of the ones that you loaded in load_data simultaneously.

### 3) hac(features)

Summary:

- Input: list of numpy arrays of shape (6,), where each array is an (x<sub>1</sub>, ..., x<sub>6</sub>) feature
    representation as computed in Section 2. The total number of feature vectors, i.e.
    the length of the input list, is *n*.
- Output: numpy array Z of the shape (*n*−1) × 4. For any *i*, Z[i,0] and Z[i,1]represent
    the indices of the two clusters that were merged in the *i*th iteration of the clustering
    algorithm. Then, Z[i,2] = d(Z[i,0], Z[i,1])is the complete linkage distance between
    the two clusters that were merged in the *i*th iteration (this will be a real value, not
    integer like the other quantities). Lastly, Z[i,3] is the size of the new cluster formed by
    the merge, i.e. the total number of Pokemon in this cluster. Note, the original Pokemon
    are considered clusters indexed by 0 , ..., *n* − 1 , and the cluster constructed in the *i*th
    iteration (i ∈ {0,1,2, ..., *n* − 2}) of the algorithm has cluster index (*n*−1) + (*i* + 1).
    Also, there is a tie-breaking rule specified below that is followed.

Details: For this function, we mimic the behavior of SciPy’s HAC function linkage().

Distance: Using complete linkage, we perform the hierarchical agglomerate clustering algo-
rith. We use the standard Euclidean distance function for calculating
the distance between two points.

**Tie Breaking:** When choosing the next two clusters to merge, we pick the pair having the
smallest complete-linkage distance. In the case that multiple pairs have the same distance,
we need additional criteria to pick between them. We do this with a tie-breaking rule on
indices as follows: Suppose(i<sub>1</sub>, j<sub>1</sub>), ...,(i<sub>h</sub>, j<sub>h</sub>) are pairs of cluster indices with equal distance, i.e., d(i<sub>1</sub>, j<sub>1</sub>) = ··· =d(i<sub>h</sub>, j<sub>h</sub>), and assume that i<sub>t</sub> < j<sub>t</sub> for all *t* (so each pair is sorted). We
tie-break by picking the pair with the smallest first index,i. If there are multiple pairs having
first index i, we need to further distinguish between them. Say these pairs are (i, t<sub>1</sub>),(i, t<sub>2</sub>), ... and so on. To tie-break between these pairs, we pick the pair with the smallest second index,
i.e., the smallest t value in these pairs. Be aware that this tie-breaking strategy may not
produce identical results tolinkage().


### 4) imshow_hac(Z)

Summary: 

- Input: numpy array Z output from hac().
- Output: None, simply plt.show() a graph that visualizes the hierarchical clustering.

### 0.5 Testing

To test the code, try running the following line in a main method or in a jupyter notebook:
hac([calc_features(row) for row in load_data('Pokemon.csv')][:n])
for various choices of n. Then compare the clustering to whatlinkage() would give you
(remember, setmethod = 'complete'), and look at the different clustering visualizations.