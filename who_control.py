from settings import *

table = pd.read_csv(table_dir)
table1 = table.dropna()\
              .groupby('LABEL')[['VAR_GL', 'VAR_G', 'VAR_L', 'CROSS_RATE', 'PITCH_CROSS_RATE', 'ROLL_CROSS_RATE']]\
              .mean()
xticklabels = [u'无操作', u'仅机长操作', u'仅副驾操作', u'共同操作']

var_gl = table1['VAR_GL']
var_g = table1['VAR_G']
var_l = table1['VAR_L']
pos = np.arange(4)
bar_width = 0.2
bias = 0.2

fig = plt.figure(figsize=(13,4), edgecolor='r')
ax1 = fig.add_subplot(121)
ax1.grid(True, axis='y', color='gray',  linestyle=':')
ax1.set_axis_bgcolor('w')
ax1.bar(pos + bias,var_gl, width=bar_width, color='#7FB1B7', linewidth=0, label=u'混合偏差的方差')
ax1.bar(pos+bias + bar_width, var_g, width=bar_width, color='#CC5B58', linewidth=0, label=u'下滑道偏差的方差')
ax1.bar(pos+bias + 2 * bar_width, var_l, width=bar_width, color='#576874', linewidth=0, label=u'航向道偏差的方差')
ax1.set_xticks(pos+ 0.5)
ax1.set_xticklabels(xticklabels, rotation=0, size='large', fontproperties=myfont)
ax1.set_ylabel(u'偏差的方差', size='large', fontproperties=myfont)

leg1 = ax1.legend(ncol=1, loc='upper left', frameon=False)
for t in leg1.get_texts():
    t.set_fontproperties(myfont)
    t.set_size('large')
    
crossRate= table1['CROSS_RATE']
pitchCrossRate = table1['PITCH_CROSS_RATE']
rollCrossRate = table1['ROLL_CROSS_RATE']
pos = np.arange(4)
bar_width = 0.2
bias = 0.2

ax2 = fig.add_subplot(122)
ax2.grid(True, axis='y', color='gray',  linestyle=':')
ax2.set_axis_bgcolor('w')
ax2.bar(pos + bias, crossRate, width=bar_width, color='#7FB1B7', linewidth=0, label=u'混合逆转率')
ax2.bar(pos+bias + bar_width, pitchCrossRate, width=bar_width, color='#CC5B58', linewidth=0, label=u'俯仰操作逆转率')
ax2.bar(pos+bias + 2 * bar_width, rollCrossRate, width=bar_width, color='#576874', linewidth=0, label=u'滚转操作逆转率')
ax2.set_xticks(pos+ 0.5)
ax2.set_xticklabels(xticklabels, rotation=0, size='large', fontproperties=myfont)
ax2.set_ylabel(u'逆转率', size='large', fontproperties=myfont)

leg2 = ax2.legend(ncol=1, loc='upper left', frameon=False)
for t in leg2.get_texts():
    t.set_fontproperties(myfont)
    t.set_size('large')
plt.show()