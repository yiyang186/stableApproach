from settings import *

table = pd.read_csv(table_dir)
blocks_num = 10
sortedRCR_VL = table.dropna().sort_values(by=['CROSS_RATE'])[['CROSS_RATE', 'VAR_GL']]
sortedRCR = sortedRCR_VL['CROSS_RATE'].values
sortedVL = sortedRCR_VL['VAR_GL'].values
blockLength = sortedRCR.size / blocks_num
start = sortedRCR.size - blockLength * 10
xticklabels = sortedRCR[start:].reshape((blocks_num, blockLength))[:,0]
xticklabels = np.concatenate((xticklabels, np.array([sortedRCR[-1]]))).round(3)
VLMeans = sortedVL[start:].reshape((blocks_num, blockLength)).mean(axis=1).round(3)
x = np.arange(VLMeans.size)

fig = plt.figure(figsize=(13,5))
ax1 = fig.add_subplot(121)
ax1.grid(True, color='gray',  linestyle=':')
ax1.plot(x + 0.5, VLMeans, c='#CC5B58')
for i in range(blocks_num):
       ax1.text(x[i] + 0.1, VLMeans[i]+0.0003, str(VLMeans[i]), fontsize='small')
ax1.set_xticks(np.arange(blocks_num+1))
ax1.set_xticklabels(xticklabels, rotation=0, size='small')
ax1.set_ylim(0.01,0.03)
ax1.set_xlabel(u'操作逆转率', fontsize='x-large', fontproperties=myfont)
ax1.set_ylabel(u'偏差的方差', fontsize='x-large', fontproperties=myfont)

nums, edges = np.histogram(sortedRCR, bins=blocks_num)
VLHistMeans = np.zeros(blocks_num)
for i in range(blocks_num):
    if nums[i] == 0:
        VLHistMeans[i] = np.nan
    else:
        VLHistMeans[i] = sortedVL[(sortedRCR > edges[i]) & (sortedRCR < edges[i+1])].sum() / nums[i]
VLHistMeans =  VLHistMeans.round(3)
edges = edges.round(3)
mask = np.isfinite(VLHistMeans)

ax2 = fig.add_subplot(122)
ax2.grid(True, color='gray',  linestyle=':')
ax2.plot(x[mask] + 0.5, VLHistMeans[mask], c='#576874')
for i in range(blocks_num):
    if mask[i]:
        ax2.text(x[i] + 0.1, VLHistMeans[i]+0.003, str(VLHistMeans[i]), fontsize='small')
ax2.set_xticks(np.arange(blocks_num+1))
ax2.set_xticklabels(edges, rotation=0, size='small')
ax2.set_xlabel(u'操作逆转率', fontsize='x-large', fontproperties=myfont)
ax2.set_ylabel(u'偏差的方差', fontsize='x-large', fontproperties=myfont)
ax2.set_ylim((0, 0.16))

ax21 = ax2.twinx()
ax21.bar(x+0.5, nums, align='center', color='#DB9982', width=1, edgecolor='w', alpha=0.4)
for i in range(blocks_num):
       ax21.text(x[i] + 0.1, nums[i]+50, str(nums[i]), fontsize='small')
ax21.set_ylabel(u'区间航段数量', fontsize='x-large', fontproperties=myfont)
ax21.set_ylim((0, 3300))
plt.show()