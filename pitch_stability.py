from settings import *

table = pd.read_csv(table_dir)
blocks_num = 10
sortedPCR_VG = table.dropna().sort_values(by=['PITCH_CROSS_RATE'])[['PITCH_CROSS_RATE', 'VAR_G']]
sortedPCR = sortedPCR_VG['PITCH_CROSS_RATE'].values
sortedVG = sortedPCR_VG['VAR_G'].values
blockLength = sortedPCR.size / blocks_num
start = sortedPCR.size - blockLength * 10
xticklabels = sortedPCR[start:].reshape((blocks_num, blockLength))[:,0]
xticklabels = np.concatenate((xticklabels, np.array([sortedPCR[-1]]))).round(3)
VGMeans = sortedVG[start:].reshape((blocks_num, blockLength)).mean(axis=1).round(3)
x = np.arange(VGMeans.size)

fig = plt.figure(figsize=(13,5))
ax1 = fig.add_subplot(121)
ax1.grid(True, color='gray',  linestyle=':')
ax1.plot(x + 0.5, VGMeans, c='#CC5B58')
for i in range(blocks_num):
       ax1.text(x[i] + 0.1, VGMeans[i]+0.001, str(VGMeans[i]), fontsize='small')
ax1.set_xticks(np.arange(blocks_num+1))
ax1.set_xticklabels(xticklabels, rotation=0, size='small')
ax1.set_xlabel(u'俯仰操作逆转率', fontsize='x-large', fontproperties=myfont)
ax1.set_ylabel(u'下滑道偏差的方差', fontsize='x-large', fontproperties=myfont)

nums, edges = np.histogram(sortedPCR, bins=blocks_num)
VGHistMeans = np.zeros(blocks_num)
for i in range(blocks_num):
    VGHistMeans[i] = sortedVG[(sortedPCR > edges[i]) & (sortedPCR < edges[i+1])].sum() / nums[i]
VGHistMeans =  VGHistMeans.round(3)
edges = edges.round(3)
ax2 = fig.add_subplot(122)
ax2.grid(True, color='gray',  linestyle=':')
ax2.plot(x + 0.5, VGHistMeans, c='#576874')
for i in range(blocks_num):
       ax2.text(x[i] + 0.1, VGHistMeans[i]+0.001, str(VGHistMeans[i]), fontsize='small')
ax2.set_xticks(np.arange(blocks_num+1))
ax2.set_xticklabels(edges, rotation=0, size='small')
ax2.set_xlabel(u'俯仰操作逆转率', fontsize='x-large', fontproperties=myfont)
ax2.set_ylabel(u'下滑道偏差的方差', fontsize='x-large', fontproperties=myfont)

ax21 = ax2.twinx()
ax21.bar(x+0.5, nums, align='center', color='#DB9982', width=1, edgecolor='w', alpha=0.4)
for i in range(blocks_num):
       ax21.text(x[i] + 0.1, nums[i]+50, str(nums[i]), fontsize='small')
ax21.set_ylabel(u'区间航段数量', fontsize='x-large', fontproperties=myfont)
plt.show()