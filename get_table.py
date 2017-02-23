from settings import *

t1 = time.time()
table = pd.DataFrame(columns=['FILENAME', 'VAR_GL', 'VAR_G', 'VAR_L', 'CROSS_RATE', 'PITCH_CROSS_RATE', 'ROLL_CROSS_RATE', 'LABEL'])
skip = 0
for i, fileName in enumerate(files):
    try:
        df = pd.read_csv(wd+fileName, usecols=usedColumns)
        df = df.fillna(method='pad')
        df = df.loc[(df['_ALTITUDE'] < 1000) & (df['_ALTITUDE'] > 100), :]
        var_g = df['_GLIDE'].var()
        var_l = df['_LOC'].var()

        sstickCapt = df[sstickCaptColumns].values.ravel()
        sstickFo = df[sstickFoColumns].values.ravel()
        hasCapt = (sstickCapt.sum() > 0)
        hasFo = (sstickFo.sum() > 0)
        if hasCapt and hasFo:
            label = 3
        elif not hasCapt and hasFo:
            label = 2
        elif hasCapt and not hasFo:
            label = 1
        else:
            label = 0

        pitchCaptSstick = df[pitchCaptColumns].values.ravel()
        pitchFoSstick = df[pitchFoColumns].values.ravel()

        pitchSstick = pitchCaptSstick + pitchFoSstick
        pitchCrossRate = ((pitchSstick[:-1] * pitchSstick[1:]) < 0).sum() / float(pitchSstick.size - 1)

        rollCaptSstick = df[rollCaptColumns].values.ravel()
        rollFoSstick = df[rollFoColumns].values.ravel()
        rollSstick = rollCaptSstick + rollFoSstick
        rollCrossRate = ((rollSstick[:-1] * rollSstick[1:]) < 0).sum() / float(rollSstick.size - 1)

        crossRate = np.diff(np.sqrt(pitchSstick ** 2 + rollSstick ** 2) > 0).sum() / float(pitchSstick.size - 1) / 2.0
        var_gl = np.sqrt(df['_GLIDE'].values ** 2 + df['_LOC'].values ** 2).var()
        new = pd.DataFrame({'FILENAME':fileName, 
                                            'VAR_GL': var_gl,
                                            'VAR_G':var_g,
                                            'VAR_L':var_l, 
                                            'CROSS_RATE': crossRate,
                                            'PITCH_CROSS_RATE':pitchCrossRate, 
                                            'ROLL_CROSS_RATE':rollCrossRate,
                                            'LABEL': label},
                                            index=[i])
        table = table.append(new, ignore_index=True)
        del df,sstickCapt, sstickFo, pitchCaptSstick, pitchFoSstick, pitchSstick, rollCaptSstick, rollFoSstick, rollSstick, new
    except:
        skip += 1
        continue
t2 = time.time()

print(skip, t2-t1)
table.to_csv(table_dir)