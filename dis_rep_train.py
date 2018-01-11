import tensorflow as tf
from hyper_params import *

pos_train_inputs = tf.placeholder(tf.int32, shape=[None], name='pos_train_input')
pos_train_labels = tf.placeholder(tf.int32, shape=[None], name='pos_train_label')
neg_train_inputs = tf.placeholder(tf.int32, shape=[None], name='neg_train_input')
neg_train_labels = tf.placeholder(tf.int32, shape=[None], name='neg_train_label')
init_width = 0.5 / user_emb_dim

user_embeddings = tf.Variable(
        tf.random_uniform([user_num, user_emb_dim],
                          -init_width, init_width,
            name="emb"))
user_weight_embeddings = tf.Variable(tf.zeros([user_num, user_emb_dim]),
                                name='weight_embeddings')
user_bias_embeddings = tf.Variable(tf.zeros([user_num]),
                              name='bias_embeddings')

pos_word_embed = tf.nn.embedding_lookup(user_embeddings, pos_train_inputs)
pos_weight_embed = tf.nn.embedding_lookup(user_weight_embeddings, pos_train_labels)
pos_bias_embed = tf.nn.embedding_lookup(user_bias_embeddings, pos_train_labels)

neg_word_embed = tf.nn.embedding_lookup(user_embeddings, neg_train_inputs)
neg_weight_embed = tf.nn.embedding_lookup(user_weight_embeddings, neg_train_labels)
neg_bias_embed = tf.nn.embedding_lookup(user_bias_embeddings, neg_train_labels)

pos_logits = tf.reduce_sum(tf.multiply(pos_word_embed, pos_weight_embed), 1) + pos_bias_embed
neg_logits = tf.reduce_sum(tf.multiply(neg_word_embed, neg_weight_embed), 1) + neg_bias_embed
# pos_logits = tf.reduce_sum(tf.multiply(pos_word_embed, pos_weight_embed), 1)
# neg_logits = tf.reduce_sum(tf.multiply(neg_word_embed, neg_weight_embed), 1)

pos_xent = tf.nn.sigmoid_cross_entropy_with_logits(
    labels=tf.ones_like(pos_logits), logits=pos_logits)
neg_xent = tf.nn.sigmoid_cross_entropy_with_logits(
    labels=tf.zeros_like(neg_logits), logits=neg_logits)

# NCE-loss is the sum of the true and noise (sampled words)
# contributions, averaged over the batch.
nce_loss_tensor = (tf.reduce_sum(pos_xent) * user_neg_batchsize+
                   tf.reduce_sum(neg_xent) ) / opts.batch_size
positive_loss = tf.reduce_sum(pos_xent) * opts.num_neg_sample/ opts.batch_size
negative_loss = tf.reduce_sum(neg_xent)  / opts.batch_size

train_tensor = tf.train.GradientDescentOptimizer(opts.lr).minimize(nce_loss_tensor)

saver_tensor = tf.train.Saver()
