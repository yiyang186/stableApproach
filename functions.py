# -*- coding:utf-8 -*-
from settings import *

table = pd.read_csv(table_dir)

# 研究操作与稳定性关系的绘图函数
def myplot(table=table,
           blocks_num=10,
           x_col='MIX_CROSS_RATE',
           y_col= 'VAR_GL',
           round_num=3,
           figsize=(13,5),
           ax1_ylim=(0.01,0.04),
           ax1_xlabel=u'逆转率',
           ax1_ylabel=u'偏差的方差',
           ax2_ylim=(0, 0.28),
           ax2_xlabel=u'逆转率',
           ax2_ylabel=u'偏差的方差',
           ax21_ylim=(0, 3600),
           ax21_xlabel=u'逆转率',
           ax21_ylabel=u'区间航段数量',
          ):
    sortedRCR_VL = table.dropna().sort_values(by=[x_col])[[x_col, y_col]]
    sortedRCR = sortedRCR_VL[x_col].values
    sortedVL = sortedRCR_VL[y_col].values
    blockLength = sortedRCR.size / blocks_num
    start = sortedRCR.size - blockLength * blocks_num
    xticklabels = sortedRCR[start:].reshape((blocks_num, blockLength))[:,0]
    xticklabels = np.concatenate((xticklabels, np.array([sortedRCR[-1]]))).round(round_num)
    VLMeans = sortedVL[start:].reshape((blocks_num, blockLength)).mean(axis=1).round(round_num)
    x = np.arange(VLMeans.size)

    fig = plt.figure(figsize=figsize)
    ax1 = fig.add_subplot(121)
    ax1.grid(True, color='gray',  linestyle=':')
    ax1.plot(x + 0.5, VLMeans, c='#CC5B58')
    for i in range(blocks_num):
           ax1.text(x[i] + 0.1, VLMeans[i]+0.0003, str(VLMeans[i]), fontsize='small')
    ax1.set_xticks(np.arange(blocks_num+1))
    ax1.set_xticklabels(xticklabels, rotation=0, size='small')
    ax1.set_ylim(ax1_ylim)
    ax1.set_xlabel(ax1_xlabel, fontsize='x-large', fontproperties=myfont)
    ax1.set_ylabel(ax1_ylabel, fontsize='x-large', fontproperties=myfont)

    nums, edges = np.histogram(sortedRCR, bins=blocks_num)
    VLHistMeans = np.zeros(blocks_num)
    for i in range(blocks_num):
        if nums[i] == 0:
            VLHistMeans[i] = np.nan
        else:
            VLHistMeans[i] = sortedVL[(sortedRCR > edges[i]) & (sortedRCR < edges[i+1])].sum() / nums[i]
    VLHistMeans =  VLHistMeans.round( round_num)
    edges = edges.round( round_num)
    mask = np.isfinite(VLHistMeans)

    ax2 = fig.add_subplot(122)
    ax2.grid(True, color='gray',  linestyle=':')
    ax2.plot(x[mask] + 0.5, VLHistMeans[mask], c='#576874')
    for i in range(blocks_num):
        if mask[i]:
            ax2.text(x[i] + 0.1, VLHistMeans[i]+0.003, str(VLHistMeans[i]), fontsize='small')
    ax2.set_xticks(np.arange(blocks_num+1))
    ax2.set_xticklabels(edges, rotation=0, size='small')
    ax2.set_xlabel(ax2_xlabel, fontsize='x-large', fontproperties=myfont)
    ax2.set_ylabel(ax2_ylabel, fontsize='x-large', fontproperties=myfont)
    ax2.set_ylim(ax2_ylim)

    ax21 = ax2.twinx()
    ax21.bar(x+0.5, nums, align='center', color='#DB9982', width=1, edgecolor='w', alpha=0.4)
    for i in range(blocks_num):
           ax21.text(x[i] + 0.1, nums[i]+50, str(nums[i]), fontsize='small')
    ax21.set_ylabel(ax21_ylabel, fontsize='x-large', fontproperties=myfont)
    ax21.set_ylim(ax21_ylim)

# 研究操作者与稳定性的关系的绘图函数
def mybar(table=table,
         groupby='LABEL',
         y_cols = ['VAR_GL', 'VAR_G', 'VAR_L'],
         figsize=(6,4),
         legends = [u'混合偏差的方差',  u'下滑道偏差的方差', u'航向道偏差的方差'],
         ylabel=u'偏差的方差'
         ):

    table_m = table.dropna().groupby(groupby)[y_cols].mean()
    table_v = table.dropna().groupby(groupby)[y_cols].std()/20
    label_num =  table.dropna().groupby(groupby).count()['FILENAME'].values
    xticklabels = [u'无操作\n{0}'.format(label_num[0]), 
                          u'仅机长操作\n{0}'.format(label_num[1]), 
                          u'仅副驾操作\n{0}'.format(label_num[2]), 
                          u'共同操作\n{0}'.format(label_num[3])]

    var_gl_m, var_gl_v = table_m[y_cols[0]], table_v[y_cols[0]]
    var_g_m, var_g_v = table_m[y_cols[1]], table_v[y_cols[1]]
    var_l_m, var_l_v = table_m[y_cols[2]], table_v[y_cols[2]]
    pos = np.arange(4)
    bar_width = 0.2
    bias = 0.2

    fig = plt.figure(figsize=figsize, edgecolor='r')
    ax1 = fig.add_subplot(111)
    ax1.grid(True, axis='y', color='gray',  linestyle=':')
    ax1.set_axis_bgcolor('w')
    ax1.bar(pos + bias, var_gl_m, width=bar_width, color='#7FB1B7', linewidth=0, yerr=var_gl_v, ecolor='black', label=legends[0])
    ax1.bar(pos+bias + bar_width, var_g_m, width=bar_width, color='#CC5B58', linewidth=0, yerr=var_g_v,ecolor='black', label=legends[1])
    ax1.bar(pos+bias + 2 * bar_width,var_l_m, width=bar_width, color='#576874', linewidth=0, yerr=var_l_v, ecolor='black',label=legends[2])
    ax1.set_xticks(pos+ 0.5)
    ax1.set_xticklabels(xticklabels, rotation=0, size='large', fontproperties=myfont)
    ax1.set_ylabel(ylabel, size='large', fontproperties=myfont)

    leg1 = ax1.legend(ncol=1, loc='upper left', frameon=False)
    for t in leg1.get_texts():
        t.set_fontproperties(myfont)
        t.set_size('large')